# Это файл, в котором будет собран основной игровой процесс
# Планирую создать несколько файлов, в которых будут классы.
# Классы импортирую сюда. И здесь соберу все вместе

class Player:
    def move(self):
        pass

    # Возвращает True, когда все корабли игрока уничтожены
    def is_looser(self) -> bool:
        return False

    # Возвращает список строк, представляющий собой поле игрока
    @property
    def board(self):
        pass


class HumanPlayer(Player):
    def __init__(self):
        # Запросить ввод расположения кораблей с клавиатуры
        pass

    def move(self):
        print("Ходит человек")

    # Возвращает список строк, представляющий собой поле игрока
    @property
    def board(self):
        return [['o' for i in range(6)] for j in range(6)]


class AiPlayer(Player):
    def __init__(self):
        # Сгенерировать положение кораблей случайным образом
        pass

    def move(self):
        print("Ходит компьютер")

    # Возвращает список строк, представляющий собой поле игрока
    @property
    def board(self):
        return [['X' for i in range(6)] for j in range(6)]


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

    def print_boards(self, player1, player2):
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
                + " | ".join(list(map(str, player1[i - 1])))
                + "\t\t"
                + str(i) + " | "
                + " | ".join(list(map(str, player2[i - 1])))
            )
        print()

    def play(self):
        human = HumanPlayer()
        ai = AiPlayer()
        player = human
        # while True:
        for i in range(10):
            self.print_boards(human.board, ai.board)
            player.move()
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
