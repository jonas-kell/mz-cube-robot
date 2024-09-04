from typing import Literal
from time import sleep
from move import move
from streamClient import CubeStream
from locations import averageColor, codeDetectionLocations
from colors import colorToString

stream = CubeStream()

frame = None


def avgColorFromLocation(
    index: int, newFrame=True
) -> Literal["red", "green", "blue", "yellow", "orange", "white"]:
    global frame

    if newFrame or frame is None:
        sleep(0.5)
        frame = stream.get_frame()
        if frame is None:
            raise Exception("Could not read frame")

    x1, y1, x2, y2 = codeDetectionLocations.get(index)

    return colorToString(averageColor(frame, x1, y1, x2, y2))


print(avgColorFromLocation(0))
move("A", True, "25")
print(avgColorFromLocation(0))
