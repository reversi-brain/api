from pydantic import BaseModel
from typing import List, Literal

# 盤面の各マスの状態 (1: 黒, -1: 白, 0: 空)
Disk = Literal[1, -1, 0]
# プレイヤー (1: 黒, -1: 白)
Player = Literal[1, -1]

class InitResponse(BaseModel):
    cells: List[Disk]
    current_player: Player
    size: int

class MoveRequest(BaseModel):
    cells: List[Disk]
    current_player: Player
    size: int
    move_index: int  # プレイヤーが置きたい場所のインデックス

class MoveResponse(BaseModel):
    cells: List[Disk]
    next_player: Player
    is_pass: bool
    is_game_over: bool
    black_count: int
    white_count: int
    message: str

class AIMoveRequest(BaseModel):
    cells: List[Disk]
    current_player: Player
    size: int