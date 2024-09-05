# Installation Instructions

## On the HOST-Computer (Laptop or whatever processes the image stream and sends the commands)

-   Install the [VS-code ev3-dev extension](https://marketplace.visualstudio.com/items?itemName=ev3dev.ev3dev-browser) if you want to interface directly with the ev3s (like for uploading files, when no network configuration up, yet).
-   Install the [VS-code Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
-   Python Extensions (in a proper `venv`, not globally):

    ```shell
    python3 -m venv .venv
    source .venv/bin/activate

    pip install --upgrade pip
    pip install --upgrade python-ev3dev2
    pip install --upgrade opencv-python
    pip install --upgrade scikit-image
    pip install --upgrade RubikTwoPhase

    ------ to deactivate
    deactivate
    ```

## On the `Raspberry Pi Zero W`

-   When Flashing the os, MAKE SURE to `enable ssh` and set password to `pi` (otherwise, you will not be able to connect to it, if you do not happen o have the proper HDMI-accessories)
-   Source code initially taken from the [official PiCamera package](http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming)
-   Make sure, the files are copied onto the devices
    -   [rpi-server](./../rpi-server.py) onto the Raspberry PI with the top level folder `mz-cube-robot`
-   Enable Camera Support

    ```shell
    sudo raspi-config
    ```

    -   Interface Options
        -   Legacy Camera support
            -   Enable
    -   RESTART

-   Install packages

    ```
    sudo apt install python3-picamera
    export PATH="/home/pi/.local/lib/python3.9/site-packages:$PATH"
    ```

-   Make the wlan interface be an Access-Point to connect to

    -   Settings to generate a Access-Point with `SSID = CUBEROBOTWLAN` and `Password = cuberobot`

        -   In that network, the `Raspberry Pi Zero W` will have the ip `192.168.1.1`, meaning, the website will be available under [http://192.168.1.1/](http://192.168.1.1/)

    -   Install Packages

    ```shell
    sudo apt install dnsmasq hostapd iptables
    ```

    -   Edit the configuration

    ```shell
    sudo nano /etc/dhcpcd.conf

    >>>>>

    interface wlan0
    static ip_address=192.168.1.1/24
    nohook wpa_supplicant
    ```

    ```shell
    sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf_alt
    sudo nano /etc/dnsmasq.conf

    >>>>>

    # DHCP-Server active for WLAN-Interface
    interface=wlan0
    # DHCP-Server not active for other networks
    no-dhcp-interface=eth0
    # IPv4-Address-Range and Lease-Time
    dhcp-range=192.168.1.100,192.168.1.200,255.255.255.0,24h
    # DNS - We
    dhcp-option=option:dns-server,192.168.1.1
    ```

    ```shell
    sudo nano /etc/hostapd/hostapd.conf

    >>>>>

    ### WLAN-Access-Point-Mode

    # Interface and driver
    interface=wlan0
    # driver=nl80211 # Commented out, may be necessary

    # WLAN-Configuration
    ssid=CUBEROBOTWLAN
    channel=1
    hw_mode=g
    ieee80211n=1
    ieee80211d=1
    country_code=DE
    wmm_enabled=1

    # WLAN-Encryption
    auth_algs=1
    wpa=2
    wpa_key_mgmt=WPA-PSK
    rsn_pairwise=CCMP
    wpa_passphrase=cuberobot
    ```

    ```shell
    sudo nano /etc/default/hostapd

    >>>>>

    RUN_DAEMON=yes
    DAEMON_CONF="/etc/hostapd/hostapd.conf"
    ```

    -   Start Service (Probably best to also reboot and see if it still works)
        -   !!! If you broke network config, you may no longer be able to connect to the device at all

    ```shell
    sudo systemctl unmask hostapd
    sudo systemctl start hostapd
    sudo systemctl enable hostapd
    ```

## On the `Lego EV3`

-   Program-wise everything should work out of the box, no extra installations required.
    -   All necessary run-times should be bundled in ev3 dev.
-   Make sure, the files are copied onto the devices
    -   [ev3-server](./../ev3-server.py) onto both ev3s with the top level folder `mz-cube-robot`
-   Further network configuration below (as it requires interaction between multiple machines)

## Network configuration (between the `Lego EV3` and the `Raspberry Pi Zero W`)

-   First follow the [connection tutorial](https://www.ev3dev.org/docs/tutorials/connecting-to-the-internet-via-usb/) to get a connection once from your desktop or laptop to the `Lego EV3`s, before you do without a GUI on the `Raspberry Pi Zero W`

    -   We want the `10.42.X.X` subnet. This is hopefully free... (otherwise Google is your friend)
        -   Adapt steps, so that you can connect to both the `Lego EV3`s and they have distinct IPv4 (see below)
    -   Enable `connect automatically`
    -   Preset the IP-Configuration Hardcoded
        -   Go in the connection menu on ev3 to `ipv4 -> load linux defaults`
            -   Now it should be `10.42.0.3` and other settings
        -   Adapt for the second one to
            -   `10.42.1.3` for ipv4
            -   `10.42.1.1` for gateway

-   Read out connections details from your compatible machine.

    ```shell
    sudo cat /etc/NetworkManager/system-connections/ev3dev.nmconnection
    ```

    -   There is an [Example Read out Connection Here](./../testing-preparation-setup/ev3-dev/ev3dev.nmconnection)
        -   The values for your `Lego EV3`s WILL BE DIFFERENT!

-   Now on the `Raspberry Pi Zero W` we can configure the interface

    -   MAC-address must be taken from the just extracted configuration!
    -   CAUTION: ! Only works when connected over lan, because this WILL reset the Access-Point Interface until Restart

    ```shell
    sudo systemctl start NetworkManager
    sudo nmcli # list the connections
    sudo nmcli connection add type ethernet ifname "*" con-name ev3dev ipv4.method shared mac 12:16:53:4A:D7:77 # Adapt to your first EV3s Mac-Address
    sudo nmcli connection add type ethernet ifname "*" con-name ev3dev-2 ipv4.method shared mac 12:16:53:4C:24:3F # Adapt to your second EV3s Mac-Address

    sudo nmcli # list the connections again, now it should be there
    ```

    -   Tell the `Lego EV3`s to reconnect, with static ips assigned
        -   At this point it may be required to swap the USB-Connections to set what will be `usb0` and `usb1`

    ```shell
    sudo ip ad add 10.42.0.1/24 dev usb0
    sudo ip ad add 10.42.1.1/24 dev usb1
    ip addr show usb0
    ip addr show usb1

    # should now have only the 10.42 entry. Delete otherwise the rest with (!! adapt ip and range !!)
    sudo ip addr del 169.254.89.145/16 dev usb0 # adapt preset ip-add/device accordingly
    ```

    -   Test if you can connect to the robot with the static ips we desire

    ```shell
    ssh -o PasswordAuthentication=yes -o PreferredAuthentications=keyboard-interactive,password -o PubkeyAuthentication=no robot@10.42.0.3

        exit

    ssh -o PasswordAuthentication=yes -o PreferredAuthentications=keyboard-interactive,password -o PubkeyAuthentication=no robot@10.42.1.3

        exit
    ```

    -   Now if that works, make it static (currently will get lost on restart)

    ```shell
    sudo ip addr del 10.42.0.1/24 dev usb0 # while still added, cannot live restart the networking because it cannot double assign
    sudo ip addr del 10.42.1.1/24 dev usb1 # while still added, cannot live restart the networking because it cannot double assign
    sudo nano /etc/network/interfaces

    >>>>>

    auto usb0
    iface usb0 inet static
        address 10.42.0.1
        netmask 255.255.255.0

    auto usb1
    iface usb1 inet static
        address 10.42.1.1
        netmask 255.255.255.0

    ```

    -   Perform restart

    ```shell
    sudo systemctl restart networking
    systemctl status networking.service
    ```

    -   Restart everything, now the [Startup Process](startup.md) should be able to be performed
