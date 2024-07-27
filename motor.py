#!/usr/bin/env python3
"""Hello to the world from ev3dev.org"""

import os
import sys

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank


# state constants
ON = True
OFF = False


def debug_print(*args, **kwargs):
    """Print debug messages to stderr.

    This shows up in the output panel in VS Code.
    """
    print(*args, **kwargs, file=sys.stderr)


def reset_console():
    """Resets the console to the default state"""
    print("\x1Bc", end="")


def set_cursor(state):
    """Turn the cursor on or off"""
    if state:
        print("\x1B[?25h", end="")
    else:
        print("\x1B[?25l", end="")


def set_font(name):
    """Sets the console font

    A full list of fonts can be found with `ls /usr/share/consolefonts`
    """
    os.system("setfont " + name)


def main():
    """The main function of our program"""

    # set the console just how we want it
    reset_console()
    set_cursor(OFF)
    set_font("Lat15-Terminus24x12")
    # setup

    print("Start")

    test = LargeMotor(OUTPUT_A)
    test.on_for_rotations(SpeedPercent(75), 5)

    debug_print("asdasd")


if __name__ == "__main__":
    main()
