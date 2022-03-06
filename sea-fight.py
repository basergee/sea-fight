# Это файл, в котором будет собран основной игровой процесс
# Планирую создать несколько файлов, в которых будут классы.
# Классы импортирую сюда. И здесь соберу все вместе

# Класс представляет результаты хода игрока: "Мимо", "Ранил", "Убил"
#
class MoveResult:
    pass


# Результаты хода игрока
#
MISSED = MoveResult()   # "Мимо"
INJURED = MoveResult()  # "Ранил"
KILLED = MoveResult()   # "Убил"


class Player:
    _own_board = []
    _enemy_board = []

    def __init__(self):
        self._own_board = [['o' for i in range(6)] for j in range(6)]
        self._enemy_board = [['o' for i in range(6)] for j in range(6)]

    # Ход игрока. Метод возвращает координаты клетки, в которую игрок
    # делает выстрел (ход)
    def make_move(self):
        pass

    # Проверяет сделанный ход. Возвращает статус: мимо, ранил, убил
    def check_move(self, coord):
        pass

    # Возвращает True, когда все корабли игрока уничтожены
    def is_looser(self) -> bool:
        return False

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
        print("\t\tИгрок \t\t\t\t\t\t\tКомпьютер")
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
                + " | ".join(list(map(str, self.own_board[i - 1])))
                + "\t\t"
                + str(i) + " | "
                + " | ".join(list(map(str, self.enemy_board[i - 1])))
            )
        print()


class HumanPlayer(Player):
    def __init__(self):
        # Запросить ввод расположения кораблей с клавиатуры
        super().__init__()

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
        return row, col

    def check_move(self, coord):
        return MISSED

    # Возвращает True, когда все корабли игрока уничтожены
    def is_looser(self) -> bool:
        return False


class AiPlayer(Player):
    def __init__(self):
        # Сгенерировать положение кораблей случайным образом
        super().__init__()
        self._own_board = [['o' for i in range(6)] for j in range(6)]
        self._enemy_board = [['x' for i in range(6)] for j in range(6)]

    def make_move(self):
        print("Ходит компьютер")
        row = 2
        col = 3
        print("Введено ", row, col)
        return row, col

    def check_move(self, coord):
        return KILLED

    # Возвращает True, когда все корабли игрока уничтожены
    def is_looser(self) -> bool:
        return True


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
        player = human
        # while True:
        for i in range(10):
            player.print_boards()
            player.make_move()
            if player.is_looser():
                break
            player = human if player == ai else ai


if __name__ == "__main__":
    game = SeaFight()
    game.print_greeting()
    game.print_help()
    game.play()


# Игровое поле 6 х 6 клеток.
# Игровое поле состоит из клеток. Часть клеток являются частями
# кораблей
#
#
#  Клетка
# --------
#
# Клетка имеет координаты
#
# Клетка имеет 4 состояния:
# - свободна
#   - не было выстрела
#   - был выстрел (промах)
# - занята кораблем
#   - не подбита
#   - подбита
#
# Каждое состояние клетки обозначается своим символом.
# Код вывода игрового поля на экран проходит по всем клеткам и
# просит клетку вывести себя на экран. Клетка выводит символ,
# соответствующий ее состоянию. А как определять переносы строк?
#
#  Корабль
# ---------
#
# Корабль состоит из клеток
# Количество клеток от 1 до 3
# Когда все клетки корабля переходят в состояние "подбита", корабль
# считается подбитым.
#
# Состояния корабля:
# - целый
# - ранен
# - подбит (убит)
#
# Игра заканчивается, когда у одного из игроков все корабли оказываются
# подбиты. Этот игрок проигрывает.
# Корабли необходимы нам для определения победителя
# .
