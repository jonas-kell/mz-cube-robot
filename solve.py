import twophase.solver as sv
from detection import detection
from time import time
from move import move

state = detection()

colorToIndexDict = {
    "white": 0,
    "red": 1,
    "yellow": 2,
    "orange": 3,
    "blue": 4,
    "green": 5,
}

colorToFaceDict = {
    "white": "U",
    "red": "F",
    "yellow": "D",
    "orange": "B",
    "blue": "R",
    "green": "L",
}

faceOffsetOrder = [
    "U",
    "R",
    "F",
    "D",
    "L",
    "B",
]

faceToMotorDict = {
    "U": ("E", False),
    "R": ("A", True),
    "F": ("D", True),
    "D": ("F", True),
    "L": ("B", True),
    "B": ("C", True),
}


cubestring = ""

for faceToPutIntoString in faceOffsetOrder:
    faceColor = list(colorToFaceDict.keys())[
        list(colorToFaceDict.values()).index(faceToPutIntoString)
    ]
    index = colorToIndexDict[faceColor]

    for i in range(3):
        for j in range(3):
            colorAtPoint = state[index, i, j]
            cubestring += colorToFaceDict[colorAtPoint]

print(f"Cubestring generated from detection: '{cubestring}'")

startSolve = time()

sol = sv.solve(cubestring, 16, 3)

print(f"solving took {time() - startSolve:.2f}s: '{sol}'")

solutionSplit = sol.split(" ")[:-1]

startExecSolve = time()

delayedMotor = "N"
delayedPercent = 25
delayedInv = False
for index, step in enumerate(solutionSplit):

    nextFace = None
    if index + 1 < len(solutionSplit):
        nextFace = solutionSplit[index + 1][0]

    face = step[0]
    steps = int(step[1])

    motor, inv = faceToMotorDict[face]

    percent = 25
    if steps == 2:
        percent = 50
    if steps == 3:
        inv = not inv

    if (nextFace, face) in [
        ("U", "D"),
        ("D", "U"),
        ("L", "R"),
        ("R", "L"),
        ("B", "F"),
        ("F", "B"),
    ]:
        print("Combine-Move")
        delayedMotor = motor
        delayedPercent = percent
        delayedInv = inv
    else:
        move(
            motor,
            inv,
            percent,
            delayedMotor,  # when prev was a Combine-Move this directly executes the double move
            delayedInv,
            delayedPercent,
        )
        delayedMotor = "N"  # reset that there is no second motor moved

print(f"executing solution took {time() - startExecSolve:.2f}s")
