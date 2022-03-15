"""
Класс Ship описывает корабль, размещаемый на игровом поле.
Объекты класса будут хранить информацию о своем положении на игровом поле,
количестве палуб и ближайшем окружении, где не должно быть других кораблей.
"""


class Ship:
    def __init__(self, coords: list):
        self._coords = []
        if len(coords) > 3 or len(coords) < 1:
            raise ValueError("Недопустимое количество палуб")
        else:
            self._coords = coords

    @property
    def number_of_decks(self):
        return len(self._coords)

    # Список координат корабля
    @property
    def coords(self):
        return self._coords

    # Возвращает список клеток вокруг корабля, в которых нельзя
    # размещать другие корабли
    @property
    def neighborhood(self):
        # Пройти по списку координат корабля и выписать координаты всех
        # окружающих корабль клеток
        neib = set()
        for row, col in self._coords:
            neib.add((row - 1, col - 1))
            neib.add((row - 1, col))
            neib.add((row - 1, col + 1))
            neib.add((row, col - 1))
            neib.add((row, col))
            neib.add((row, col + 1))
            neib.add((row + 1, col - 1))
            neib.add((row + 1, col))
            neib.add((row + 1, col + 1))

        # neib содержит окрестность каждой клетки корабля. Теперь надо убрать
        # клетки за пределами игрового поля
        neib = set(filter(
            lambda cell: 0 <= cell[0] < 6 and 0 <= cell[1] < 6,
            neib
        ))

        return neib
