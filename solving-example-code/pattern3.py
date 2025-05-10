from move import move

# compatible, run this 2 times and then pattern2.py

move("E", False, "25", "F", False, "25")
for i in range(2):
    move("E", False, "25")
    move("D", False, "50")
    move("E", True, "25")
    move("B", True, "25")
    move("C", False, "50")
    move("B", False, "25")
move("E", True, "25", "F", True, "25")
