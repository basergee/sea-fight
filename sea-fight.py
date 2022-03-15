"""
Главный модуль игры "Морской бой"

Здесь расположен класс SeaFight, отвечающий за игровой процесс и вывод на экран
информации для пользователя
"""

import random

from board import MISSED
from board import INJURED
from board import KILLED
from human_player import HumanPlayer
from ai_player import AiPlayer
from human_player import WrongMoveError


def main():
    new_game = True
    while new_game:
        game = SeaFight()
        game.print_greeting()
        game.print_help()
        game.ask_show_ai_board()
        game.play()
        while True:
            s = input("Хотите начать новую игру [y (Да) / n (Нет)]?: ")
            if s == 'y':
                break
            elif s == 'n':
                new_game = False
                break
            print("Введите 'y' или 'n'")


class SeaFight:
    def __init__(self):
        self._show_ai_board = True

    def print_greeting(self):
        #    ("123456789_123456789_123456789_123456789_123456789_123456789_12")
        print("+------------------------------------------------------------+")
        print("|                     Морской бой                            |")
        print("+------------------------------------------------------------+")

    def print_help(self):
        #    ("123456789_123456789_123456789_123456789_123456789_123456789_12")
        print("+------------------------------------------------------------+")
        print("| Игра на поле 6х6 против компьютера. Очередь первого хода   |")
        print("| определяется случайным образом. Расположение кораблей как  |")
        print("| компьютера, так и игрока определяется случайным образом.   |")
        print("| Побеждает тот, кто первым уничтожит все корабли противника.|")
        print("| После победы одного из игроков на экран будет выведено     |")
        print("| игровое поле победителя.                                   |")
        print("+------------------------------------------------------------+")

    def ask_show_ai_board(self):
        while True:
            s = input("Показывать игровое поле компьютера "
                      "[y (Да) / n (Нет)]?: ")
            if s == 'y':
                self._show_ai_board = True
                break
            elif s == 'n':
                self._show_ai_board = False
                break
            print("Введите 'y' или 'n'")

    def play(self):
        human = HumanPlayer()
        ai = AiPlayer()

        # Первый ход делает игрок player1. Случайным образом определяем, кто
        # это: человек или компьютер. Вероятность того, что это будет человек,
        # можно менять, меняя цифру справа от знака неравенства
        player1 = human if random.randint(0, 9) > 5 else ai
        player2 = ai if player1 is human else human
        while True:
            human.print_boards()
            if self._show_ai_board:
                ai.print_boards()
            try:
                result = player2.check_move(player1.make_move())
            except WrongMoveError:
                print("Нельзя стрелять в одну клетку дважды!")
                print("Сделайте другой ход")
                continue
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
    main()
