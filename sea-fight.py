
# Класс представляет результаты хода игрока: "Мимо", "Ранил", "Убил"
#
import random


class MoveResult:
    pass


# Результаты хода игрока
#
MISSED = MoveResult()   # "Мимо"
INJURED = MoveResult()  # "Ранил"
KILLED = MoveResult()   # "Убил"


class WrongMoveError(Exception):
    pass


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

    def set_cell(self, coord: (int, int), move_result: MoveResult):
        row, col = coord
        if move_result == MISSED:
            self._board[row][col] = 'T'
        elif move_result == INJURED or move_result == KILLED:
            self._board[row][col] = 'X'

    # Обновляет состояние клетки, заданой координатами (строка, столбец).
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


class Player:
    def __init__(self):
        self._own_board = Board()
        self._enemy_board = Board()

    # Ход игрока. Метод возвращает координаты клетки, в которую игрок
    # делает выстрел (ход)
    def make_move(self):
        pass

    # Проверяет сделанный ход. Возвращает статус: мимо, ранил, убил
    def check_move(self, coord):
        pass

    # Обновляет игровые поля в соответствии с результатом хода
    def update_boards(self, move_result: MoveResult):
        pass

    # Возвращает True, когда все корабли игрока уничтожены
    def is_looser(self) -> bool:
        return self.own_board.number_of_ships == 0

    # Возвращает список строк, представляющий собой поле игрока
    @property
    def own_board(self):
        return self._own_board

    # Возвращает список строк, представляющий собой поле соперника
    @property
    def enemy_board(self):
        return self._enemy_board

    def print_boards(self):
        # Делаем отступ от любого предыдущего вывода
        print()

        # Выводим горизонтальную ось координат на две доски
        print(
            "  | " + " | ".join(map(str, range(1, 7)))
            + "\t\t"
            + "  | " + " | ".join(map(str, range(1, 7)))
        )

        # К каждой строке клеток добавляем первым символом цифру оси
        # координат
        for i in range(1, 7):
            print(
                str(i) + " | "
                + " | ".join(list(map(str, self.own_board.as_list[i - 1])))
                + "\t\t"
                + str(i) + " | "
                + " | ".join(list(map(str, self.enemy_board.as_list[i - 1])))
            )
        print()


class HumanPlayer(Player):
    def __init__(self):
        # Запросить ввод расположения кораблей с клавиатуры
        super().__init__()
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

    def check_move(self, coord):
        row, col = coord
        return self._own_board.update_cell((row - 1, col - 1))

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


class AiPlayer(Player):

    def __init__(self):
        # Сгенерировать положение кораблей случайным образом
        super().__init__()
        self._own_board = Board()
        self._enemy_board = Board()

        # Список возможных ходов. Из них будем случайно выбирать ход
        self._moves = [(i, j) for i in range(1, 7) for j in range(1, 7)]
        random.shuffle(self._moves)

        # Создаем корабли. Один 3-х палубный, два 2-х палубных, четыре
        # однопалубных. Повторяем процедуру заново, если хотя бы один корабль
        # попал в окрестность другого корабля

        # Если корабль вертикальный 3-х палубный, то координата 0 <= row <= 3
        # Если корабль горизонтальный 3-х палубный, то координата 0 <= col <= 3
        # Если корабль вертикальный 2-х палубный, то координата 0 <= row <= 4
        # Если корабль горизонтальный 2-х палубный, то координата 0 <= col <= 4

        ships = []
        while True:
            # Создадим 3-х палубный корабль. Он задается координатами одного
            # угла и ориентацией. В случае горизонтального расположения
            # считаем созданную координату координатой левой палубы корабля.
            # В случае вертикального расположения -- считаем координатой
            # верхней палубы корабля
            row, col = random.randint(0, 3), random.randint(0, 3)

            # По умолчанию, корабль расположен горизонтально. Мы случайным
            # образом решаем, расположить ли корабль вертикально. Вероятность
            # вертикального расположения корабля можно менять, меняя цифру
            # справа от знака неравенства '>'.
            coords = [(row, col), (row, col + 1), (row, col + 2)]
            if random.randint(0, 9) > 5:
                # Корабль расположим вертикально
                coords = [(row, col), (row + 1, col), (row + 2, col)]
            ships.append(Ship(coords))

            # Аналогично создадим два 2-х палубных корабля. К 2-х палубным
            # кораблям предъявляется дополнительное требование. Все части
            # корабля должны находиться на расстоянии 1 клетка от 3-х палубного
            # и от других кораблей
            for i in range(2):
                row, col = random.randint(0, 4), random.randint(0, 4)
                coords = [(row, col), (row, col + 1)]
                if random.randint(0, 9) > 5:
                    # Корабль расположим вертикально
                    coords = [(row, col), (row + 1, col)]

                # Проверяем, что ни одна часть корабля не попадает в
                # окрестность другого корабля
                reset = False
                for s in ships:
                    for deck in coords:
                        if deck in s.neighborhood:
                            reset = True
                            break

                # Какой-то корабль попал в окрестность другого корабля
                # Повторить генерацию кораблей
                if reset:
                    ships.clear()
                    break

                ships.append(Ship(coords))

            # Создаем 4 однопалубных корабля. Ни один из них не должен попасть
            # в окрестность других кораблей
            for i in range(4):
                row, col = random.randint(0, 5), random.randint(0, 5)

                # Проверяем, что корабль не попадает в окрестность другого корабля
                reset = False
                for s in ships:
                    if (row, col) in s.neighborhood:
                        reset = True
                        break

                # Какой-то корабль попал в окрестность другого корабля
                # Повторить генерацию кораблей
                if reset:
                    ships.clear()
                    break

                ships.append(Ship([(row, col)]))

            # Всего должно быть создано 7 кораблей
            if len(ships) == 7:
                break

        # Корабли успешно созданы, добавляем их на игровое поле
        for s in ships:
            self._own_board.add_ship(s)

    # Возвращает координаты клетки, куда делается ход. Ход делается
    # случайно. Метод всегда возвращает допустимые координаты
    def make_move(self):
        print("Ходит компьютер")
        m = self._moves[-1]
        print("Ходы компа: ", self._moves)
        print("Введено ", *m)
        return m

    def check_move(self, coord):
        row, col = coord
        return self._own_board.update_cell((row - 1, col - 1))

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


class SeaFight:
    def print_greeting(self):
        #    ("123456789_123456789_123456789_123456789_123456789_123456789_12")
        print("+------------------------------------------------------------+")
        print("|                     Морской бой                            |")
        print("+------------------------------------------------------------+")

    def print_help(self):
        #    ("123456789_123456789_123456789_123456789_123456789_123456789_12")
        print("+------------------------------------------------------------+")
        print("| Игра на поле 6х6 против компьютера. Очередь первого хода   |")
        print("| определяется случайным образом. Побеждает тот, кто первым  |")
        print("| уничтожит все корабли противника.                          |")
        print("|                                                            |")
        print("+------------------------------------------------------------+")

    def play(self):
        human = HumanPlayer()
        ai = AiPlayer()
        player1 = human
        player2 = ai
        while True:
            human.print_boards()
            ai.print_boards()
            result = player2.check_move(player1.make_move())
            player1.update_boards(result)
            print("Ответ противника: ", end="")
            if result == INJURED:
                print("Ранил")
                continue
            elif result == KILLED:
                print("Убил")
                if player2.is_looser():
                    if player2 == human:
                        print("Победил компьютер!")
                    elif player2 == ai:
                        print("Победил игрок!")

                    print("Игровое поле победителя:")
                    player1.print_boards()
                    break
            elif result == MISSED:
                print("Мимо")
                # Ход переходит другому игроку
                player1, player2 = player2, player1


if __name__ == "__main__":
    game = SeaFight()
    game.print_greeting()
    game.print_help()
    game.play()
