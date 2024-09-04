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
