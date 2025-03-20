from typing import Tuple, List
from time import sleep, time
from move import move
from streamClient import CubeStream
from locations import averageColor, codeDetectionLocations
import numpy as np
import os


def save_array(arr, filename="calibrate.npy"):
    """Saves a NumPy array to a file in the script's directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get script directory
    file_path = os.path.join(script_dir, filename)
    np.save(file_path, arr)


def load_array(filename="calibrate.npy"):
    """Loads a NumPy array from a file in the script's directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get script directory
    file_path = os.path.join(script_dir, filename)
    return np.load(file_path)


stream = CubeStream()

frame = None


def avgColorFromLocation(index: int, newFrame=True) -> Tuple[int, int, int]:
    global frame

    if newFrame or frame is None:
        sleep(0.6)
        frame = stream.get_frame()
        if frame is None:
            raise Exception("Could not read frame")

    x1, y1, x2, y2 = codeDetectionLocations.get(index)

    avg = averageColor(frame, x1, y1, x2, y2)

    return (int(avg[0]), int(avg[1]), int(avg[2]))


calibrationState = np.array(
    [
        [  # white
            [0, 0, 0],  # 0
            [0, 0, 0],  # 1
            [0, 0, 0],  # 2
            [0, 0, 0],  # 3
            [0, 0, 0],  # 4
            [0, 0, 0],  # 5
            [0, 0, 0],  # 6
            [0, 0, 0],  # 7
            [0, 0, 0],  # 8
            [0, 0, 0],  # 9
            [0, 0, 0],  # 10
            [0, 0, 0],  # 11
            [0, 0, 0],  # 12
            [0, 0, 0],  # 13
        ],
        [  # red
            [0, 0, 0],  # 0
            [0, 0, 0],  # 1
            [0, 0, 0],  # 2
            [0, 0, 0],  # 3
            [0, 0, 0],  # 4
            [0, 0, 0],  # 5
            [0, 0, 0],  # 6
            [0, 0, 0],  # 7
            [0, 0, 0],  # 8
            [0, 0, 0],  # 9
            [0, 0, 0],  # 10
            [0, 0, 0],  # 11
            [0, 0, 0],  # 12
            [0, 0, 0],  # 13
        ],
        [  # yellow
            [0, 0, 0],  # 0
            [0, 0, 0],  # 1
            [0, 0, 0],  # 2
            [0, 0, 0],  # 3
            [0, 0, 0],  # 4
            [0, 0, 0],  # 5
            [0, 0, 0],  # 6
            [0, 0, 0],  # 7
            [0, 0, 0],  # 8
            [0, 0, 0],  # 9
            [0, 0, 0],  # 10
            [0, 0, 0],  # 11
            [0, 0, 0],  # 12
            [0, 0, 0],  # 13
        ],
        [  # orange
            [0, 0, 0],  # 0
            [0, 0, 0],  # 1
            [0, 0, 0],  # 2
            [0, 0, 0],  # 3
            [0, 0, 0],  # 4
            [0, 0, 0],  # 5
            [0, 0, 0],  # 6
            [0, 0, 0],  # 7
            [0, 0, 0],  # 8
            [0, 0, 0],  # 9
            [0, 0, 0],  # 10
            [0, 0, 0],  # 11
            [0, 0, 0],  # 12
            [0, 0, 0],  # 13
        ],
        [  # blue
            [0, 0, 0],  # 0
            [0, 0, 0],  # 1
            [0, 0, 0],  # 2
            [0, 0, 0],  # 3
            [0, 0, 0],  # 4
            [0, 0, 0],  # 5
            [0, 0, 0],  # 6
            [0, 0, 0],  # 7
            [0, 0, 0],  # 8
            [0, 0, 0],  # 9
            [0, 0, 0],  # 10
            [0, 0, 0],  # 11
            [0, 0, 0],  # 12
            [0, 0, 0],  # 13
        ],
        [  # green
            [0, 0, 0],  # 0
            [0, 0, 0],  # 1
            [0, 0, 0],  # 2
            [0, 0, 0],  # 3
            [0, 0, 0],  # 4
            [0, 0, 0],  # 5
            [0, 0, 0],  # 6
            [0, 0, 0],  # 7
            [0, 0, 0],  # 8
            [0, 0, 0],  # 9
            [0, 0, 0],  # 10
            [0, 0, 0],  # 11
            [0, 0, 0],  # 12
            [0, 0, 0],  # 13
        ],
    ],
)


def setColorFromIndex(colorIndex: int, photoIndex: int, newFrame=True):
    global calibrationState

    calibrationState[colorIndex, photoIndex] = avgColorFromLocation(
        photoIndex, newFrame=newFrame
    )


def recordColors(control: List[Tuple[int, int, int, int]]):
    for index, [colorIndex, photoIndex] in enumerate(control):
        setColorFromIndex(colorIndex, photoIndex, index == 0)


def calibration():
    startOfDetection = time()

    recordColors(
        [
            (1, 7),
            (1, 8),
            (1, 9),
            (1, 10),
            (1, 11),
            (1, 12),
            (1, 13),
            #
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (0, 5),
            (0, 6),
        ]
    )
    move("A", True, "25", "B", False, "25")
    recordColors(
        [
            (2, 7),
            (2, 9),
            (2, 10),
            (2, 11),
            (2, 12),
            (2, 13),
            #
            (1, 0),
            (1, 2),
            (1, 3),
            (1, 4),
            (1, 5),
            (1, 6),
        ]
    )
    move("A", True, "25", "B", False, "25")
    recordColors(
        [
            (3, 7),
            (3, 9),
            (3, 10),
            (3, 11),
            (3, 12),
            (3, 13),
            #
            (2, 0),
            (2, 2),
            (2, 3),
            (2, 4),
            (2, 5),
            (2, 6),
        ]
    )
    move("A", True, "25", "B", False, "25")
    recordColors(
        [
            (0, 7),
            (0, 9),
            (0, 10),
            (0, 11),
            (0, 12),
            (0, 13),
            #
            (3, 0),
            (3, 2),
            (3, 3),
            (3, 4),
            (3, 5),
            (3, 6),
        ]
    )
    move("A", True, "25", "B", False, "25")

    # fixed

    move("C", True, "25", "D", False, "25")
    recordColors(
        [
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 5),
            (4, 6),
        ]
    )
    move("C", True, "50", "D", False, "50")
    recordColors(
        [
            (5, 0),
            (5, 1),
            (5, 2),
            (5, 5),
            (5, 6),
        ]
    )
    move("C", True, "25", "D", False, "25")

    # fixed

    move("E", True, "25", "F", True, "25")
    recordColors(
        [
            (5, 7),
            (5, 8),
            (5, 9),
            (5, 12),
            (5, 13),
        ]
    )
    move("E", True, "50", "F", True, "50")
    recordColors(
        [
            (4, 7),
            (4, 8),
            (4, 9),
            (4, 12),
            (4, 13),
        ]
    )
    move("E", True, "25", "F", True, "25")

    # fixed

    move("D", False, "25")
    move("B", False, "25")
    move("E", True, "25")

    recordColors(
        [
            (0, 8),
            (1, 1),
        ]
    )

    move("E", False, "25")
    move("B", True, "25")
    move("D", True, "25")

    # fixed

    move("A", True, "25", "B", False, "25")
    move("D", True, "25")
    recordColors(
        [
            (2, 8),
        ]
    )
    move("D", False, "25")
    move("A", True, "25", "B", False, "25")
    move("D", True, "25")
    recordColors(
        [
            (3, 8),
        ]
    )
    move("D", False, "25")
    move("E", True, "25")
    recordColors(
        [
            (2, 1),
        ]
    )
    move("E", False, "25")
    move("A", True, "25", "B", False, "25")

    move("E", True, "25")
    recordColors(
        [
            (3, 1),
        ]
    )
    move("E", False, "25")
    move("A", True, "25", "B", False, "25")

    # fixed

    move("C", True, "25", "D", False, "25")
    move("E", True, "25")
    recordColors(
        [
            (4, 3),
            (4, 4),
        ]
    )
    move("A", False, "25", "B", True, "25")
    recordColors(
        [
            (4, 10),
            (4, 11),
        ]
    )
    move("A", True, "25", "B", False, "25")
    move("E", False, "25")
    move("C", True, "50", "D", False, "50")
    move("E", True, "25")
    recordColors(
        [
            (5, 3),
            (5, 4),
        ]
    )
    move("A", False, "25", "B", True, "25")
    recordColors(
        [
            (5, 10),
            (5, 11),
        ]
    )
    move("A", True, "25", "B", False, "25")
    move("E", False, "25")
    move("C", True, "25", "D", False, "25")

    # fixed

    print(f"calibration took {time() - startOfDetection:.2f}s")

    return calibrationState


if __name__ == "__main__":
    cal = calibration()
    save_array(cal)

    print(load_array())
