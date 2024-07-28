import ev3_dc as ev3

# https://pypi.org/project/ev3-dc/

my_ev3 = ev3.EV3(protocol=ev3.USB)
my_ev3.verbosity = 1
ops = b"".join(
    (
        ev3.opSound,
        ev3.TONE,
        ev3.LCX(1),  # VOLUME
        ev3.LCX(440),  # FREQUENCY
        ev3.LCX(1000),  # DURATION
    )
)
my_ev3.send_direct_cmd(ops)
