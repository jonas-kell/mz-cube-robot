from typing import Dict, Tuple, Literal
import numpy as np
import colorsys
from skimage import color

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


def rgb_to_lab(r: int, g: int, b: int):
    rgb_normalized = np.array([r, g, b]) / 255.0
    lab = color.rgb2lab(rgb_normalized)
    return lab[0:3]  # l, a, b


def euclidean_distance_lab(color1_lab, color2_lab):
    return np.linalg.norm(color1_lab - color2_lab)


colors = {
    "red": [210, 23, 38],
    "orange": [210, 132, 84],
    "green": [13, 166, 49],
    "blue": [0, 20, 173],
    "white": [121, 161, 223],
    "yellow": [207, 224, 63],
}
colors_lab = {name: rgb_to_lab(r, g, b) for name, (r, g, b) in colors.items()}


# https://colorizer.org/
def colorToString(
    col: Tuple[int, int, int]
) -> Literal["red", "green", "blue", "yellow", "orange", "white"]:
    r, g, b = col

    input_lab = rgb_to_lab(r, g, b)

    current = "red"
    currentDistance = euclidean_distance_lab(input_lab, colors_lab["red"])
    for comparisonColorName, comparisonColorLab in colors_lab.items():
        newDist = euclidean_distance_lab(comparisonColorLab, input_lab)
        if newDist < currentDistance:
            currentDistance = newDist
            current = comparisonColorName

    return current
