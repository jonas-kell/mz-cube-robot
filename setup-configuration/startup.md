# Startup procedure

## First Time

-   Perform all the steps in [Hardware Setup](./hardware-configuration.md)
-   Perform all the steps in [Installation](./installation-instructions.md)
-   Make sure, the files are copied onto the devices
    -   [ev3-server](./../ev3-server.py) onto both ev3s with the top level folder `mz-cube-robot`
    -   [rpi-server](./../rpi-server.py) onto the Raspberry PI with the top level folder `mz-cube-robot`

## Subsequent Boots

-   Start both `Lego EV3`s FIRST. And wait until they have booted fully (takes some time)
-   THEN start the Raspberry Pi (if started too early, the `Lego EV3`s will not get properly mapped to their network devices)
-   SSH connections (Perform the commands below in order):
    -   SSH onto pi: default user: `pi`, pw: `pi`
    -   SSH onto ev3 FROM THE PI (only there the USB-Connection is established): default user: `robot`, pw: `maker`

```shell
ssh -o PasswordAuthentication=yes -o PreferredAuthentications=keyboard-interactive,password -o PubkeyAuthentication=no pi@192.168.1.1

    ssh -o PasswordAuthentication=yes -o PreferredAuthentications=keyboard-interactive,password -o PubkeyAuthentication=no robot@10.42.0.3

        sudo python3 ~/mz-cube-robot/ev3-server.py # enter pw, when started abort with ctrl + c
        nohup sudo python3 ~/mz-cube-robot/ev3-server.py &

        exit

    ssh -o PasswordAuthentication=yes -o PreferredAuthentications=keyboard-interactive,password -o PubkeyAuthentication=no robot@10.42.1.3

        sudo python3 ~/mz-cube-robot/ev3-server.py # enter pw, when started abort with ctrl + c
        nohup sudo python3 ~/mz-cube-robot/ev3-server.py &

        exit

    sudo python3 ~/mz-cube-robot/rpi-server.py # enter pw, when started abort with ctrl + c
    nohup sudo python3 ~/mz-cube-robot/rpi-server.py &

    exit
```

This makes sure, that all server programs are running on the devices and the console ssh-connections can be terminated.
