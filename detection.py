from typing import Literal, Tuple, List
from time import sleep, time
from move import move
from streamClient import CubeStream
from locations import averageColor, codeDetectionLocations
from colors import colorToString
import numpy as np

stream = CubeStream()

frame = None


def avgColorFromLocation(
    index: int, newFrame=True
) -> Literal["red", "green", "blue", "yellow", "orange", "white"]:
    global frame

    if newFrame or frame is None:
        sleep(0.6)
        frame = stream.get_frame()
        if frame is None:
            raise Exception("Could not read frame")

    x1, y1, x2, y2 = codeDetectionLocations.get(index)

    return colorToString(averageColor(frame, x1, y1, x2, y2))


state = np.array(
    [
        [
            ["black", "black", "black"],
            ["black", "white", "black"],
            ["black", "black", "black"],
        ],
        [
            ["black", "black", "black"],
            ["black", "red", "black"],
            ["black", "black", "black"],
        ],
        [
            ["black", "black", "black"],
            ["black", "yellow", "black"],
            ["black", "black", "black"],
        ],
        [
            ["black", "black", "black"],
            ["black", "orange", "black"],
            ["black", "black", "black"],
        ],
        [
            ["black", "black", "black"],
            ["black", "blue", "black"],
            ["black", "black", "black"],
        ],
        [
            ["black", "black", "black"],
            ["black", "green", "black"],
            ["black", "black", "black"],
        ],
    ]
)


def setColorFromIndex(
    photoIndex: int, faceIndex: int, rowIndex: int, colIndex: int, newFrame=True
):
    global state

    state[faceIndex, rowIndex, colIndex] = avgColorFromLocation(
        photoIndex, newFrame=newFrame
    )


def recordColors(control: List[Tuple[int, int, int, int]]):
    for index, [photoIndex, faceIndex, rowIndex, colIndex] in enumerate(control):
        setColorFromIndex(photoIndex, faceIndex, rowIndex, colIndex, index == 0)


def detection():
    startOfDetection = time()

    recordColors(
        [
            (0, 0, 2, 2),
            (3, 0, 1, 2),
            (5, 0, 0, 2),
            (2, 0, 2, 0),
            (4, 0, 1, 0),
            (6, 0, 0, 0),
            #
            (7, 1, 0, 2),
            (10, 1, 1, 2),
            (12, 1, 2, 2),
            (9, 1, 0, 0),
            (11, 1, 1, 0),
            (13, 1, 2, 0),
            #
            (1, 0, 2, 1),
            (8, 1, 0, 1),
        ]
    )
    move("A", True, "50", "B", False, "50")
    recordColors(
        [
            (0, 2, 2, 2),
            (3, 2, 1, 2),
            (5, 2, 0, 2),
            (2, 2, 2, 0),
            (4, 2, 1, 0),
            (6, 2, 0, 0),
            #
            (7, 3, 2, 0),
            (10, 3, 1, 0),
            (12, 3, 0, 0),
            (9, 3, 2, 2),
            (11, 3, 1, 2),
            (13, 3, 0, 2),
        ]
    )
    move("A", True, "50", "B", False, "50")

    move("E", True, "25", "F", True, "25")
    move("D", True, "25", "C", False, "25")
    recordColors(
        [
            (4, 0, 0, 1),
            #
            (1, 5, 1, 2),
            #
            (7, 5, 0, 0),
            (10, 5, 0, 1),
            (12, 5, 0, 2),
            (9, 5, 2, 0),
            (11, 5, 2, 1),
            (13, 5, 2, 2),
        ]
    )
    move("A", True, "50", "B", False, "50")
    recordColors(
        [
            (4, 2, 2, 1),
            (3, 2, 0, 1),
            #
            (7, 4, 0, 0),
            (10, 4, 0, 1),
            (12, 4, 0, 2),
            (9, 4, 2, 0),
            (11, 4, 2, 1),
            (13, 4, 2, 2),
        ]
    )
    move("A", True, "50", "B", False, "50")
    move("D", False, "25", "C", True, "25")
    move("E", False, "25", "F", False, "25")

    move("D", False, "25", "C", True, "25")
    move("E", True, "25")
    recordColors(
        [
            (10, 1, 2, 1),
            #
            (3, 4, 1, 0),
            (4, 4, 1, 2),
        ]
    )
    move("E", False, "25")
    move("D", True, "25", "C", False, "25")

    move("C", False, "25")
    move("A", False, "25", "B", True, "25")
    move("E", False, "50")
    recordColors(
        [
            (1, 5, 1, 0),
            #
            (3, 3, 2, 1),
            (4, 3, 0, 1),
        ]
    )
    move("E", False, "50")
    move("A", True, "25", "B", False, "25")
    move("C", True, "25")

    print(f"detection took {time() - startOfDetection:.2f}s")

    whiteNumber = np.sum(state == "white")
    yellowNumber = np.sum(state == "yellow")
    redNumber = np.sum(state == "red")
    orangeNumber = np.sum(state == "orange")
    greenNumber = np.sum(state == "green")
    blueNumber = np.sum(state == "blue")
    if (
        whiteNumber != 9
        or yellowNumber != 9
        or redNumber != 9
        or orangeNumber != 9
        or greenNumber != 9
        or blueNumber != 9
    ):
        print(state)
        raise Exception("Not a possible cube configuration")

    return state


if __name__ == "__main__":
    print(detection())
