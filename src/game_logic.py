from typing import List
from src.models import Disk, Player

DIRECTIONS = [
    (-1, 0), (-1, 1), (0, 1), (1, 1),
    (1, 0), (1, -1), (0, -1), (-1, -1)
]

def get_initial_board(size: int = 8) -> List[Disk]:
    """初期盤面を生成する"""
    cells = [0] * (size * size)
    center_row = size // 2
    center_col = size // 2
    cells[(center_row - 1) * size + (center_col - 1)] = -1
    cells[(center_row - 1) * size + center_col] = 1
    cells[center_row * size + (center_col - 1)] = 1
    cells[center_row * size + center_col] = -1
    return cells

def get_flippable_disks(index: int, player: Player, cells: List[Disk], size: int) -> List[int]:
    """指定したマスに石を置いた場合、裏返せるマスのインデックス配列を返す"""
    if cells[index] != 0:
        return []

    row = index // size
    col = index % size
    flippable = []

    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        flipped_in_dir = []

        while 0 <= r < size and 0 <= c < size:
            target_index = r * size + c
            target_disk = cells[target_index]

            if target_disk == 0:
                break
            if target_disk == player:
                flippable.extend(flipped_in_dir)
                break
            
            flipped_in_dir.append(target_index)
            r += dr
            c += dc

    return flippable

def has_valid_moves(player: Player, cells: List[Disk], size: int) -> bool:
    """指定したプレイヤーが打てる場所が存在するか判定する"""
    for i in range(len(cells)):
        if cells[i] == 0 and len(get_flippable_disks(i, player, cells, size)) > 0:
            return True
    return False