"""
Класс Board представляет собой игровое поле размером 6х6 клеток, на котором
размещаются корабли. Класс отвечает за хранение информации о размещенных
кораблях и результатох ходов. Именно этот класс проверяет, каким был результат
очередного хода.
"""


# Класс представляет результаты хода игрока: "Мимо", "Ранил", "Убил"
#
class MoveResult:
    pass


# Результаты хода игрока
#
MISSED = MoveResult()   # "Мимо"
INJURED = MoveResult()  # "Ранил"
KILLED = MoveResult()   # "Убил"


class Board:
    def __init__(self):
        self._board = [['o' for i in range(6)] for j in range(6)]
        self._ships = []

    @property
    def number_of_ships(self):
        return len(self._ships)

    @property
    def as_list(self):
        return self._board

    def add_ship(self, ship):
        for row, col in ship.coords:
            self._board[row][col] = '■'

        self._ships.append(ship)

    # Ставит символ в клетку, соответствующий результатам хода
    def set_cell(self, coord: (int, int), move_result: MoveResult):
        row, col = coord
        if move_result == MISSED:
            self._board[row][col] = 'T'
        elif move_result == INJURED or move_result == KILLED:
            self._board[row][col] = 'X'

    # Обновляет состояние клетки, заданной координатами (строка, столбец).
    # Считается, что в эту клетку произведен выстрел.
    # Возвращает результат: мимо, ранил, убил
    def update_cell(self, coord: (int, int)) -> MoveResult:
        for ship in self._ships:
            if coord in ship.coords:
                self.set_cell(coord, INJURED)
                if all([self._board[row][col] == 'X' for row, col in ship.coords]):
                    self._ships.remove(ship)
                    return KILLED
                return INJURED
        self.set_cell(coord, MISSED)
        return MISSED
