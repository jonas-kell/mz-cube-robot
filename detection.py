import requests
from typing import Literal
import cv2
import urllib3
import numpy as np
from time import sleep

url = "http://192.168.1.1/stream.mjpg"


class MJPEGStream:
    def __init__(self):
        pass

    def get_frame(self):
        self.http = urllib3.PoolManager()
        self.response = self.http.request("GET", url, preload_content=False)
        self.bytes = b""
        try:
            while True:
                chunk = self.response.read(1024)
                self.bytes += chunk
                a = self.bytes.find(b"\xff\xd8")
                b = self.bytes.find(b"\xff\xd9")

                if a != -1 and b != -1:
                    jpg = self.bytes[a : b + 2]
                    self.bytes = self.bytes[b + 2 :]
                    frm = cv2.imdecode(
                        np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR
                    )
                    self.response.release_conn()
                    return frm  # Return the captured frame

        except Exception as e:
            print(f"Error: {e}")
            return None  # Return None if there's an error


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


def readAverageColor(x1: int, y1: int, x2: int, y2: int, frame):
    print(frame)


stream = MJPEGStream()

frame = stream.get_frame()
if frame is not None:
    readAverageColor(frame)

move("A", True, "25")
# move("B", True, "25")
# move("C", True, "25")
# move("D", True, "25")

sleep(0.5)

# frame = stream.get_frame()
# if frame is not None:
#     cv2.imshow("Single Frame 2", frame)
#     cv2.waitKey(300)
# move("E", False, "25")
# move("F", False, "25")
