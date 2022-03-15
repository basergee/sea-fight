"""
Класс AiPlayer представляет игрока Компьютер. Он делает случайные выстрелы и не
повторяет свои ходы.
"""

import random

from player import Player
from board import MoveResult


class AiPlayer(Player):
    def __init__(self):
        # Сгенерировать положение кораблей случайным образом
        super().__init__()
        self.fill_board()

        # Список возможных ходов. Из них будем случайно выбирать ход
        self._moves = [(i, j) for i in range(1, 7) for j in range(1, 7)]
        random.shuffle(self._moves)

    # Возвращает координаты клетки, куда делается ход. Ход делается
    # случайно. Метод всегда возвращает допустимые координаты
    def make_move(self):
        print("Ходит компьютер")
        m = self._moves[-1]
        print("Введено ", *m)
        return m

    # Обновляет игровые поля в соответствии с результатом хода
    def update_boards(self, move_result: MoveResult):
        # Берем координаты последнего хода и обновляем доску в соответствии с ними
        prev_move_row = self._moves[-1][0] - 1
        prev_move_col = self._moves[-1][1] - 1
        self.enemy_board.set_cell((prev_move_row, prev_move_col), move_result)
        self._moves.pop(-1)

    def print_boards(self):
        # Делаем отступ от любого предыдущего вывода
        print()
        print("\tИгрок (компьютер) \t\t\t\t\tПротивник")
        super().print_boards()
