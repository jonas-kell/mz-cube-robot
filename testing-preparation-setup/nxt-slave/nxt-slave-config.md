# Legacy: talk to NXT2.0

[Last commit, where this was used](https://github.com/jonas-kell/mz-cube-robot/blob/22c137ebf0f76d9267865a2a87c0837d4efc5210/rpi-server.py).

This was scrapped due to not solvable motor precision errors when using `Lego NXT 2.0`.

```cmd
# required installations on the raspberry pi zero w to get the nxt-communication package to work
pip install --upgrade pip
pip install --upgrade nxt-python
pip install --upgrade pyusb
```

It was tried, to make this run on the `Lego EV3`, as it has a USB-Host port and could control the `Lego NXT 2.0`.
This was however unsuccessful, to the python version in [ev3dev](https://www.ev3dev.org/) and the requirement for the control pip lib [nxt-python](https://github.com/schodet/nxt-python).

Therefor, the `Raspberry Pi Zero W` was chosen to issue the commands to the `Lego NXT 2.0`.

-   [Main test](discover.py)

Direct Control (running motors commands directly over USB) is way to imprecise.
This is because the device reading the motor encoder and issuing start/stop is incapable to do so effectively due to the USB-delay.

-   [Direct Control EV3](ev3_slave.py)
-   [Direct Control NXT](nxt_slave.py)

The "solution" that reduced that problem, was to run code locally on the `Lego NXT 2.0` that turns the motors and only communicate the direction/speed/amount over serial communication, eliminating the inaccuracy.

The programs were written in [Open Roberta Lab](https://lab.open-roberta.org/), as this is a nice - still supported - way to program the legacy `Lego NXT 2.0`.

The setup how to talk to the robot was under the `Open Roberta Wiki` under `»Set Up«`. This has moved to a confluence site with required login, since, so I refuse to write down links to the details now...

The programs that used the bluetooth communication api to read the message how far and which motor to turn are [Here](./messagemotor.xml).
Attempts were made, to [run motors in parallel](./messagemotorparallel.xml) that were fully unsuccessful.

[Some example how to write messages (text/numbers)](./message.py) to the `Lego NXT 2.0`.

[This server implementation](https://github.com/jonas-kell/mz-cube-robot/blob/22c137ebf0f76d9267865a2a87c0837d4efc5210/rpi-server.py) used a second message channel that was checked for message box empty-nes, because writing messages back into the box from nxt was unsuccessful and so this was the only way I fond to communicate back to the server that we are done.

## END

In the end still motor positioning of any of these was not sufficiently precise enough for repeated use in the final application.
