"""
Класс HumanPlayer представляет игрока Человека. Он запрашивает координаты
клетки, в которую произвести выстрел, у пользователя. Если пользователь
пытается выстрелить в одну и ту же клетку несколько раз, выбрасывается
исключение.
"""

from player import Player
from board import MoveResult


# При повторном ходе в одну и ту же клетку выбрасывается это исключение
class WrongMoveError(Exception):
    pass


class HumanPlayer(Player):
    def __init__(self):
        # Запросить ввод расположения кораблей с клавиатуры
        super().__init__()
        self.fill_board()
        self._moves = []

    # Возвращает координаты клетки, куда делается ход, которые
    # запрашивает у пользователя. Выбрасывает исключение
    # WrongMoveError, если ход повторяет ранее сделанный ход
    def make_move(self):
        print("Ходит игрок")

        row = None  # Номер строки
        col = None  # Номер столбца

        while True:
            try:
                row = int(input("Введите номер строки: "))
            except ValueError:
                print("Введите ЧИСЛО!")
                continue

            if 1 <= row <= 6:
                break
            else:
                print("За пределами игрового поля")
                print("Повторите ввод")

        while True:
            try:
                col = int(input("Введите номер столбца: "))
            except ValueError:
                print("Введите ЧИСЛО!")
                continue

            if 1 <= col <= 6:
                break
            else:
                print("За пределами игрового поля")
                print("Повторите ввод")

        print("Введено ", row, col)
        if (row, col) not in self._moves:
            self._moves.append((row, col))
            return row, col
        else:
            raise WrongMoveError("Вы уже стреляли в эту клетку!")

    # Обновляет игровые поля в соответствии с результатом хода
    def update_boards(self, move_result: MoveResult):
        # Берем координаты последнего хода и обновляем доску в соответствии с ними
        prev_move_row = self._moves[-1][0] - 1
        prev_move_col = self._moves[-1][1] - 1
        self.enemy_board.set_cell((prev_move_row, prev_move_col), move_result)

    def print_boards(self):
        # Делаем отступ от любого предыдущего вывода
        print()
        print("\tИгрок (человек) \t\t\t\t\tПротивник")
        super().print_boards()
