from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.models import InitResponse, MoveRequest, MoveResponse
from src import game_logic

app = FastAPI(
    title="Reversi Brain API",
    description="オセロのコアロジックとAIを提供するAPIサーバー",
    version="1.0.0"
)

# Web（Next.js）からの通信を許可する設定 (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Reversi Brain API is running!"}
@app.post("/api/init", response_model=InitResponse)
def initialize_game(size: int = 8):
    """ゲーム開始時の初期盤面データを返す"""
    if size % 2 != 0 or size < 4:
        raise HTTPException(status_code=400, detail="Size must be an even number >= 4")
    
    cells = game_logic.get_initial_board(size)
    return InitResponse(
        cells=cells,
        current_player=1,
        size=size
    )
@app.post("/api/move", response_model=MoveResponse)
def make_move(request: MoveRequest):
    """プレイヤーの手を受け取り、裏返しやパス・終了判定を行って新しい盤面を返す"""
    cells = list(request.cells)
    player = request.current_player
    size = request.size
    
    # 1. 裏返せる石を計算
    flippable = game_logic.get_flippable_disks(request.move_index, player, cells, size)
    
    # 2. ルール違反（裏返せない場所への配置）はエラーとして弾く
    if not flippable:
        raise HTTPException(status_code=400, detail="Invalid move")
        
    # 3. 石を置く＆裏返す
    cells[request.move_index] = player
    for idx in flippable:
        cells[idx] = player
        
    # 4. 次の手番とパス・ゲーム終了判定
    next_player = -1 if player == 1 else 1
    has_next = game_logic.has_valid_moves(next_player, cells, size)
    
    is_pass = False
    is_game_over = False
    
    if has_next:
        current_turn_player = next_player
    else:
        # 次のプレイヤーが打てない場合、現在のプレイヤーがもう一度打てるか確認
        has_current = game_logic.has_valid_moves(player, cells, size)
        if has_current:
            is_pass = True
            current_turn_player = player
        else:
            is_game_over = True
            current_turn_player = player
            
    # 5. 石の数をカウント
    black_count = cells.count(1)
    white_count = cells.count(-1)
    
    msg = "Success"
    if is_game_over:
        msg = "Game Over"
    elif is_pass:
        msg = f"{'Black' if next_player == 1 else 'White'} passed."
        
    return MoveResponse(
        cells=cells,
        next_player=current_turn_player,
        is_pass=is_pass,
        is_game_over=is_game_over,
        black_count=black_count,
        white_count=white_count,
        message=msg
    )
