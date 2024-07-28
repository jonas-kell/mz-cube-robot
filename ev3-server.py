import socket
from ev3dev2.motor import (
    LargeMotor,
    OUTPUT_A,
    OUTPUT_B,
    OUTPUT_C,
    OUTPUT_D,
    SpeedPercent,
)
import re


# url_callback: provided function, that takes the following inputs:
#     the method of the request
#     the url of the request
#
#     and that returns the result-string to be echoed back to the client
def startServer(ipv4, url_callback):
    # HTTP-Server starten
    if ipv4 != "":
        print("Start Server")
        addr = socket.getaddrinfo(ipv4, 80)[0][-1]
        server = socket.socket()
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(addr)
        server.listen(1)
        print("Server is listening to ", addr)
        print()
        print("In interactive mode the server can be shut down with CTRL + C")
        print()

    # Auf eingehende Verbindungen hören
    while True:
        try:
            conn, addr = server.accept()
            print("HTTP-Request recieved from Client", addr)
            request = conn.recv(1024)
            request = str(request)
            request = request.split()

            print(request)

            method = request[0].lstrip("'b")
            url = request[1].lstrip("'b")

            print("METHOD:", method)
            print("URL:", url)

            # Process by user defined function:
            resp = url_callback(method, url)

            conn.send(
                bytes("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n", "utf-8")
            )
            conn.send(bytes(resp, "utf-8"))
            conn.close()

            print("Sent HTTP-Response ")
            print()
        except OSError as e:
            break
        except KeyboardInterrupt:
            break

    try:
        conn.close()
    except NameError:
        pass
    try:
        server.close()
    except NameError:
        pass
    print("Server Exited")


# //TODO more robust version that can decode urlencoded stuff.
# first returns the url_string, then the parameters as object
def parseUrl(url):
    parameters = {}
    url_string = url.split("?")[0] if "?" in url else url
    query_string = url.split("?")[1] if "?" in url else ""

    if query_string:
        pairs = query_string.split("&")
        for pair in pairs:
            key_value = pair.split("=")
            if len(key_value) == 2:
                key = key_value[0]
                value = key_value[1]
                parameters[key] = value

    return url_string, parameters


# [(port, minus, percent)]
def parse_string(input_string: str):
    pattern = re.compile(r"^([ABCD](-?(25|50|75|100)&))+$")
    if (
        not pattern.match(input_string)
        or input_string.count("A") > 1
        or input_string.count("B") > 1
        or input_string.count("C") > 1
        or input_string.count("D") > 1
    ):
        return []

    print("check through")

    parts = input_string.split("&")
    result = []
    for part in parts:
        match = re.match(r"^([ABCD])(-?)(25|50|75|100)$", part)
        if match:
            letter, minus, value = match.groups()
            result.append((letter, minus == "-", int(value)))

    return result


def run_motor(port, minus, percent):
    ports = {"A": OUTPUT_A, "B": OUTPUT_B, "C": OUTPUT_C, "D": OUTPUT_D}
    motor = LargeMotor(ports[port])
    motor.on_for_rotations(100, percent / 100.0, True, False)

    return motor


def motor_callback(method, url):
    print(method, url)

    command = url.lstrip("/")

    instructions = parse_string(command)

    if len(instructions) == 0:
        return "nothing\n"

    try:
        motors = []
        for port, minus, percent in instructions:
            motor = run_motor(port, minus, percent)
            motors.append(motor)

        for motor in motors:
            motor.wait_until_not_moving(1000)
    except Exception as e:
        return "error\n"

    return "success\n"


startServer("0.0.0.0", motor_callback)
