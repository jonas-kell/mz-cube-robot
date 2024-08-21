import requests
from typing import Literal


def move(
    motor: Literal["A", "B", "C", "D", "E", "F"],
    minus: bool,
    deg: Literal["25", "50", "75", "100"],
    motor2: Literal["N", "A", "B", "C", "D", "E", "F"] = "N",
    minus2: bool = False,
    deg2: Literal["25", "50", "75", "100"] = "25",
):
    if motor2 == "N":
        requests.get(
            f"http://192.168.1.1/{motor}{'-' if minus else ''}{deg}&", timeout=2
        )
    else:
        requests.get(
            f"http://192.168.1.1/{motor}{'-' if minus else ''}{deg}&{motor2}{'-' if minus2 else ''}{deg2}&",
            timeout=2,
        )


move("A", True, "25", "B", True, "25")
move("B", True, "25")
move("C", True, "25")
move("D", True, "25")
move("E", True, "25")
move("F", True, "25")
