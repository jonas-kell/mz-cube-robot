from move import move


move("A", True, "25")
move("B", True, "25")
move("C", True, "25")
move("D", True, "25")
move("E", True, "25")
move("F", True, "25")

move("A", False, "100")
move("B", False, "100")
move("C", False, "100")
move("D", False, "100")
move("E", False, "100")
move("F", False, "100")

move("A", True, "50", "B", True, "50")
move("C", True, "50", "D", True, "50")
move("E", True, "50", "F", False, "50")
