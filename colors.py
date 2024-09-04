from typing import Tuple, Literal
import numpy as np
from skimage import color


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

    # method relatively bad in discening orange and red. Therefore do extra comparison, that is basically a hsl comparison
    # scale by the lightness, given by red channel (because the shade yould be either lighter or darker)
    # information red/orange then is basically contained in the green channel
    if current == "red" or current == "orange":
        lightness_scaler = (r - 130) / (220 - 130)  # approximately 0-1
        region = 0.35  # defines the "intensity" how strongly the lighting factor is taken into account
        lightness_score = (
            region + (1 - 2 * region) * lightness_scaler
        )  # definitely 0-100 with extremes not that bad
        green_score = g / lightness_score
        if green_score < 100:  # empirical
            current = "red"
        else:
            current = "orange"

    return current
