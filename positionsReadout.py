import cv2
import urllib3
import numpy as np
from locations import codeDetectionLocations, colorToString, averageColor
from url import url


def drawOnImage(
    image,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    index: str,
    text: str,
):
    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
    cv2.putText(
        image,
        text,
        (x1 + 10, y2 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.3,
        (0, 0, 0),
        1,
    )
    cv2.putText(
        image,
        index,
        (x1 + 10, y2 - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.3,
        (0, 0, 0),
        1,
    )


stream_url = f"{url}/stream.mjpg"
http = urllib3.PoolManager()
try:
    response = http.request("GET", stream_url, preload_content=False)
    stream = response.stream(1024)

    bytes = b""
    for chunk in stream:
        bytes += chunk
        a = bytes.find(b"\xff\xd8")
        b = bytes.find(b"\xff\xd9")

        if a != -1 and b != -1:
            jpg = bytes[a : b + 2]
            bytes = bytes[b + 2 :]

            # Note: The cv2.CV_LOAD_IMAGE_COLOR flag is not needed in newer OpenCV versions
            i = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            for index in codeDetectionLocations:
                (x1, y1, x2, y2) = codeDetectionLocations.get(index)
                drawOnImage(
                    i,
                    x1,
                    y1,
                    x2,
                    y2,
                    str(index),
                    colorToString(averageColor(i, x1, y1, x2, y2)),
                )
            cv2.imshow("i", i)

            if cv2.waitKey(1) == 27:
                exit(0)

except Exception as e:
    print(f"Error: {e}")
