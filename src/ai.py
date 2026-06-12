import random
from typing import List
from src.models import Disk, Player
from src import game_logic

def get_random_move(player: Player, cells: List[Disk], size: int) -> int:
    """打てる場所（合法手）の中からランダムに1つ選ぶ弱いAI"""
    valid_moves = []
    
    # 盤面のすべてのマスをチェックして、打てる場所を探す
    for i in range(len(cells)):
        if cells[i] == 0:
            flippable = game_logic.get_flippable_disks(i, player, cells, size)
            if flippable:  # 裏返せる石があれば、そこは合法手
                valid_moves.append(i)
                
    # もし打てる場所が1つもなければ -1（パス）を返す
    if not valid_moves:
        return -1
        
    # 合法手の中からランダムに1つのインデックスを選んで返す
    return random.choice(valid_moves)