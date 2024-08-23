from typing import Dict, Tuple
import numpy as np

codeDetectionLocations: Dict[
    int,
    Tuple[
        int,  # x1
        int,  # y1
        int,  # x2
        int,  # y2
    ],
] = {0: (201, 174, 268, 208)}


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


def colorToString(col: Tuple[int, int, int]) -> str:
    return f"{col[0]:.0f}, {col[1]:.0f}, {col[2]:.0f}"
