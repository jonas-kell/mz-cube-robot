import cv2
import urllib3
import numpy as np
from url import url


stream_url = f"{url}/stream.mjpg"


class CubeStream:
    def __init__(self):
        pass

    def get_frame(self):
        self.http = urllib3.PoolManager()
        self.response = self.http.request("GET", stream_url, preload_content=False)
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
