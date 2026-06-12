from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.models import InitResponse, MoveRequest, MoveResponse, AIMoveRequest
from src import game_logic
from src import ai

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
    if size % 2 != 0 or size < 4:
        raise HTTPException(status_code=400, detail="Size must be an even number >= 4")
    cells = game_logic.get_initial_board(size)
    return InitResponse(cells=cells, current_player=1, size=size)
@app.post("/api/move", response_model=MoveResponse)
def make_move(request: MoveRequest):
    """人間のプレイヤーが石を置くときのエンドポイント"""
    cells = list(request.cells)
    player = request.current_player
    size = request.size
    
    flippable = game_logic.get_flippable_disks(request.move_index, player, cells, size)
    if not flippable:
        raise HTTPException(status_code=400, detail="Invalid move")
        
    cells[request.move_index] = player
    for idx in flippable:
        cells[idx] = player
        
    return _process_turn_end(cells, player, size)
@app.post("/api/ai-move", response_model=MoveResponse)
def make_ai_move(request: AIMoveRequest):
    """AI（CPU）に次の一手を考えさせて石を置くエンドポイント"""
    cells = list(request.cells)
    player = request.current_player
    size = request.size
    
    # AIに次の一手を考えさせる
    move_index = ai.get_random_move(player, cells, size)
    
    # もし打てる場所がなかった場合（パス）
    if move_index == -1:
        return _process_turn_end(cells, player, size, is_force_pass=True)
        
    # 打つ場所が決まったら、実際に裏返し処理を行う
    flippable = game_logic.get_flippable_disks(move_index, player, cells, size)
    cells[move_index] = player
    for idx in flippable:
        cells[idx] = player
        
    return _process_turn_end(cells, player, size)
def _process_turn_end(cells: list, player: int, size: int, is_force_pass: bool = False):
    """人間とAIで共通して使う、ターン終了時の判定処理（パス・勝敗判定）"""
    next_player = -1 if player == 1 else 1
    
    if is_force_pass:
        has_next = game_logic.has_valid_moves(next_player, cells, size)
        if has_next:
            return MoveResponse(cells=cells, next_player=next_player, is_pass=True, is_game_over=False, black_count=cells.count(1), white_count=cells.count(-1), message="Passed.")
        else:
            return MoveResponse(cells=cells, next_player=player, is_pass=False, is_game_over=True, black_count=cells.count(1), white_count=cells.count(-1), message="Game Over")
    has_next = game_logic.has_valid_moves(next_player, cells, size)
    is_pass = False
    is_game_over = False
    
    if has_next:
        current_turn_player = next_player
    else:
        has_current = game_logic.has_valid_moves(player, cells, size)
        if has_current:
            is_pass = True
            current_turn_player = player
        else:
            is_game_over = True
            current_turn_player = player
            
    return MoveResponse(
        cells=cells, next_player=current_turn_player, is_pass=is_pass, is_game_over=is_game_over,
        black_count=cells.count(1), white_count=cells.count(-1),
        message="Game Over" if is_game_over else ("Passed." if is_pass else "Success")
    )