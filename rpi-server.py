import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
import re
import requests

PAGE = """\
<html>
<head>
<title>Cube-Solver-Camera</title>
</head>
<body>
<center><h1>Cube-Solver-Camera</h1></center>
<center><img src="stream.mjpg" width="640" height="480"></center>
<center>
    <p>
        <a href="/A25&amp;" target="_blank" onclick="event.preventDefault(); fetch(this.href).then(response => response.text()).then(data => console.log(data)).catch(error => console.error('Error:', error));">
            Rotate A ( /A25&amp; )
        </a>
    </p>
    <p>
        <a href="/B25&amp;" target="_blank" onclick="event.preventDefault(); fetch(this.href).then(response => response.text()).then(data => console.log(data)).catch(error => console.error('Error:', error));">
            Rotate B ( /B25&amp; )
        </a>
    </p>
    <p>
        <a href="/C25&amp;" target="_blank" onclick="event.preventDefault(); fetch(this.href).then(response => response.text()).then(data => console.log(data)).catch(error => console.error('Error:', error));">
            Rotate C ( /C25&amp; )
        </a>
    </p>
    <p>
        <a href="/D25&amp;" target="_blank" onclick="event.preventDefault(); fetch(this.href).then(response => response.text()).then(data => console.log(data)).catch(error => console.error('Error:', error));">
            Rotate D ( /D25&amp; )
        </a>
    </p>
    <p>
        <a href="/E25&amp;" target="_blank" onclick="event.preventDefault(); fetch(this.href).then(response => response.text()).then(data => console.log(data)).catch(error => console.error('Error:', error));">
            Rotate E ( /E25&amp; )
        </a>
    </p>
    <p>
        <a href="/F25&amp;" target="_blank" onclick="event.preventDefault(); fetch(this.href).then(response => response.text()).then(data => console.log(data)).catch(error => console.error('Error:', error));">
            Rotate F ( /F25&amp; )
        </a>
    </p>
</center>
</body>
</html>
"""


class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b"\xff\xd8"):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)


# [(port, minus, percent)]
def parse_string(input_string: str):
    pattern = re.compile(r"^([ABCDEF](-?(25|50|75|100)&))+$")
    if (
        not pattern.match(input_string)
        or input_string.count("A") > 1
        or input_string.count("B") > 1
        or input_string.count("C") > 1
        or input_string.count("D") > 1
        or input_string.count("E") > 1
        or input_string.count("F") > 1
    ):
        return None

    parts = input_string.split("&")
    result = []
    for part in parts:
        match = re.match(r"^([ABCDEF])(-?)(25|50|75|100)$", part)
        if match:
            letter, minus, value = match.groups()
            result.append((letter, minus == "-", int(value)))

    return result


class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        didSomething = False

        if self.path == "/":
            didSomething = True
            self.send_response(301)
            self.send_header("Location", "/index.html")
            print("Top Level required")
            self.end_headers()
        elif self.path == "/index.html":
            didSomething = True
            content = PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", len(content))
            self.end_headers()
            print("Index required")
            self.wfile.write(content)
        elif self.path == "/stream.mjpg":
            didSomething = True
            self.send_response(200)
            self.send_header("Age", 0)
            self.send_header("Cache-Control", "no-cache, private")
            self.send_header("Pragma", "no-cache")
            self.send_header(
                "Content-Type", "multipart/x-mixed-replace; boundary=FRAME"
            )
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b"--FRAME\r\n")
                    self.send_header("Content-Type", "image/jpeg")
                    self.send_header("Content-Length", len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b"\r\n")
            except Exception as e:
                logging.warning(
                    "Removed streaming client %s: %s", self.client_address, str(e)
                )

        command = self.path.lstrip("/")

        instructions = parse_string(command)

        if instructions is not None and len(instructions) == 0:
            didSomething = True
            content = "nothing".encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", len(content))
            self.end_headers()
            self.wfile.write(content)

        if instructions is not None and len(instructions) != 0:
            didSomething = True
            state = "\n"

            ## control motors

            try:
                # forward to ev3 server 1
                ev3URL = "http://10.42.0.3/"
                ev3count = 0
                for port, minus, percent in instructions:
                    if port == "A" or port == "B" or port == "C" or port == "D":
                        ev3URL += f"{port}{'-' if minus else ''}{percent}&"
                        ev3count += 1
                if ev3count > 0:
                    print(f"Forwarding request {ev3URL} to ev3")
                    response = requests.get(ev3URL, timeout=2)
                    response.raise_for_status()
                    state = response.text
            except Exception as e:
                print(e)
                state = "error\n"

            if state != "error":
                try:
                    # forward to ev3 server 2
                    ev3URL = "http://10.42.1.3/"
                    ev3count = 0
                    for port, minus, percent in instructions:
                        if port == "E" or port == "F":
                            if port == "E":
                                port = "A"
                            if port == "F":
                                port = "B"

                            ev3URL += f"{port}{'-' if minus else ''}{percent}&"
                            ev3count += 1
                    if ev3count > 0:
                        print(f"Forwarding request {ev3URL} to ev3")
                        response = requests.get(ev3URL, timeout=2)
                        response.raise_for_status()
                        state = response.text
                except Exception as e:
                    print(e)
                    state = "error\n"

            ## control motors

            content = state.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", len(content))
            self.end_headers()
            self.wfile.write(content)

        # fallback
        if not didSomething:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


with picamera.PiCamera(resolution="640x480", framerate=30) as camera:
    output = StreamingOutput()
    camera.rotation = 180
    camera.shutter_speed = 3500
    camera.start_recording(output, format="mjpeg")
    try:
        address = ("0.0.0.0", 80)
        print("Starting server on ", address)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
