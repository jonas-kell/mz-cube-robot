import cv2
import urllib3
import numpy as np

url = "http://192.168.1.1/stream.mjpg"
http = urllib3.PoolManager()
try:
    response = http.request("GET", url, preload_content=False)
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
            cv2.imshow("i", i)

            if cv2.waitKey(1) == 27:
                exit(0)

except Exception as e:
    print(f"Error: {e}")
