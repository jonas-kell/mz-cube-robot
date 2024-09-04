from typing import Dict, Tuple, Literal
import numpy as np
import colorsys

codeDetectionLocations: Dict[
    int,
    Tuple[
        int,  # x1
        int,  # y1
        int,  # x2
        int,  # y2
    ],
] = {
    0: (177, 176, 249, 228),
    1: (272, 170, 343, 217),
    2: (368, 170, 430, 222),
    3: (194, 250, 254, 286),
    4: (370, 242, 423, 281),
    5: (206, 310, 270, 340),
    6: (367, 302, 416, 331),
    7: (182, 123, 238, 154),
    8: (273, 122, 340, 149),
    9: (361, 118, 441, 148),
    10: (197, 81, 249, 106),
    11: (355, 81, 423, 102),
    12: (203, 53, 254, 72),
    13: (347, 49, 410, 68),
}


def averageColor(
    image,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
) -> Tuple[int, int, int]:
    slice = image[y1:y2, x1:x2]
    flat = slice.reshape(-1, slice.shape[-1])
    average = np.average(flat, axis=0)
    b, g, r = average
    return (r, g, b)


def colorToString(
    col: Tuple[int, int, int]
) -> Literal["red", "green", "blue", "yellow", "orange", "white"]:
    r, g, b = col

    rprime = r / 255.0
    gprime = g / 255.0
    bprime = b / 255.0

    h, l, s = colorsys.rgb_to_hls(rprime, gprime, bprime)

    h, l, s = h * 360, l * 100, s * 100

    if l > 70:
        return "white"

    colors = {
        "red": 0,
        "green": 100,
        "yellow": 60,
        "orange": 20,
        "blue": 250,
    }

    current = "red"
    currentDistance = 700
    for comparisonColor, comparisonHue in colors.items():
        newDist = min(abs(comparisonHue - h), abs(abs(comparisonHue - h) - 360))
        if newDist < currentDistance:
            currentDistance = newDist
            current = comparisonColor

    return current
