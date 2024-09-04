from move import move
from random import randrange

motors = ["A", "B", "C", "D", "E", "F"]
percentages = [25, 50, 75]

numScrambleMoves = 20

for _ in range(numScrambleMoves):
    motor = motors[randrange(0, 6)]
    percentage = percentages[randrange(0, 3)]
    dir = randrange(0, 10) % 2 == 0

    move(motor, dir, percentage)
