import random

class Player:
    def __init__(self):
        self.cards = [random.randint(1, 9) for _ in range(5)]

class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.table = []

    def start(self):
        print("Початкові картки гравців:")
        print("Гравець 1:", self.player1.cards)
        print("Гравець 2:", self.player2.cards)

        while self.player1.cards and self.player2.cards:
            card1 = self.player1.cards.pop()
            card2 = self.player2.cards.pop()

            print("\nГравець 1 викладає картку:", card1)
            print("Гравець 2 викладає картку:", card2)

            self.table.append(card1)
            if len(self.table) > 1 and card1 == self.table[-2]:
                self.player2.cards.insert(0, card1)

            self.table.append(card2)
            if len(self.table) > 1 and card2 == self.table[-2]:
                self.player1.cards.insert(0, card2)

            print("Картки на столі:", self.table)

            if card1 == 7 or card2 == 7:
                print("\nГра закінчена: викладено картку з цифрою 7")
                break

        total = sum(self.table)
        if total % 2 == 0:
            return "Перший гравець переміг оскільки на столі парна кількість очок"
        else:
            return "Другий гравець переміг оскільки на столі непарна кількість очок"
