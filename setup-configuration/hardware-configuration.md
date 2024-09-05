# Hardware Configuration

How to setup the hardware:

## Raspberry Pi Setup

-   Connect the Power-Port with the Micro-USB Cable to the 5V Power-Supply
-   Connect the Data-Port to the Micro-USB to USB-A-female Adapter and plug the USB-Hub into this.
    -   Into this, you plug the USB-A sides of the cables that lead to the `Lego EV3`s
    -   Optional: USB-A to ethernet adapter to have LAN-Connectivity to the contraption
-   Get the LEDs to shine with the resistor and the jumper wires (breadboards or soldering required) ([Tutorial](https://www.elektronik-kompendium.de/sites/raspberry-pi/2102181.htm))
    -   [Pinout of the raspberry pi zero](https://pinout.xyz/pinout/io_pi_zero)
        -   I used 2,4 for one side and 6,14 for the other (check polarity of LED)
-   Flash the OS to one of the micro SD-Cards
    -   [Tutorial, to follow for Camera Setup](https://www.conrad.de/de/ratgeber/schule-unterricht/raspberry-pi/ueberwachungskamera-mit-raspberry-pi.html)
    -   [Flashing Program: Raspberry Pi Imager](https://www.raspberrypi.com/software/)
        -   When Flashing the os, make sure to `enable ssh` and set password to `pi`
        -   [Which OS?](https://www.raspberrypi.com/software/operating-systems/)
            -   Raspberry Pi OS (other)
                -   Raspberry Pi OS (Legacy - 32 bit) Lite
    -   Insert into the SD-Card Slot
-   Connect the camera module to the raspberry Pi Zero

## EV3 Setup (Both completely the same)

-   Power Management
    -   Either load with 6AA batteries each
    -   OR connect 9V Wall brick to the power terminals
        -   best to get a connection to the terminal, by wedging Aluminum-Foil/Tinfoil onto the contacts with one AA battery
            -   (the battery just has the correct size, will not be part of the circuit, may also be an empty one)
            -   Check Polarity and which terminal to use
            -   Best to use a Multimeter to check Voltage (9V) and Polarity (see image)
            -   Power supply should provide 4A, lower specs may result in the brick shutting down under load
-   Flash the [ev3dev](https://www.ev3dev.org/docs/getting-started/) onto the remaining two SD-Cards
    -   Can also use Raspberry Pi Imager for this task
    -   Insert the SD-Cards into the `Lego EV3` slot
-   Connect the USB-Cables to the USB-Hub (keep the connection, generally the same configuration. Swapping them may break the assignment in the Network Manager, later)
-   Build your Model (Requires your creativity and a lot of Lego-Parts)
    -   Your freedom of design choice.
        -   Should connect one motor to every face of the cube
        -   Motors should spin freely, the cube nicely in the center
        -   Space for the camera to view at least two sides of the cube (the more you can easily see, the easier the detection)
        -   Mount the LEDs, so that they can be powered and still illuminate the cube faces nicely

<table style="width: 100%; border-collapse: collapse; border: none;">
    <tr>
        <td style="text-align: center; vertical-align: middle;">
            <img src="../files/RPiCabeling.jpg" style="max-width: 45vw; max-height: 80vh;">
        </td>
        <td style="text-align: center; vertical-align: middle;">
            <img src="../files/PowerSetupEv3.jpg" style="max-width: 45vw; max-height: 80vh;">
        </td>
    </tr>
</table>
<table style="width: 100%; border-collapse: collapse; border: none;">
    <tr>
        <td style="text-align: center; vertical-align: middle;">
            <img src="../files/BuildOverview.jpg" style="max-width: 90vw; max-height: 80vh;">
        </td>
    </tr>
</table>
