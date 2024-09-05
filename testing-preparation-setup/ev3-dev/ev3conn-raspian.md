Follow the connection tutorial:

https://www.ev3dev.org/docs/tutorials/connecting-to-the-internet-via-usb/

Read out connection details on a compatible machine.

```cmd
sudo cat /etc/NetworkManager/system-connections/ev3dev.nmconnection
```

Now on the pi w we can configure the interface:
(mac address must be taken from the just extracted configuration)

(Only works when connected over lan, because this will reset the wlan router)

```cmd
sudo systemctl start NetworkManager
sudo nmcli # list the connections
sudo nmcli connection add type ethernet ifname "*" con-name ev3dev ipv4.method shared mac 12:16:53:4A:D7:77
sudo nmcli connection add type ethernet ifname "*" con-name ev3dev-2 ipv4.method shared mac 12:16:53:4C:24:3F

sudo nmcli # list the connections again, now it should be there
```

Tell the ev3 to reconnect, then we have a new ip assigned.
Then go in the connection menu on ev3 to "load linux defaults". now it should be `10.42.0.3` / (adapt for the second one to) `10.42.1.3` for ipv4 and `10.42.1.1` for gateway.

```cmd
sudo ip ad add 10.42.0.1/24 dev usb0
sudo ip ad add 10.42.1.1/24 dev usb1
ip addr show usb0
ip addr show usb1

# should now have only the 10.42 entry. Delete otherwise the rest with (adapt ip and range)
sudo ip addr del 169.254.89.145/16 dev usb0 # or adapt ip-add/device accordingly (or restart device)
```

```cmd
ssh -o PasswordAuthentication=yes -o PreferredAuthentications=keyboard-interactive,password -o PubkeyAuthentication=no robot@10.42.0.3
```

Now if that works, make it static:

```cmd
sudo ip addr del 10.42.0.1/24 dev usb0 # if still added, cannot live restart
sudo ip addr del 10.42.1.1/24 dev usb1 # if still added, cannot live restart
sudo nano /etc/network/interfaces


--------
auto usb0
iface usb0 inet static
    address 10.42.0.1
    netmask 255.255.255.0

auto usb1
iface usb1 inet static
    address 10.42.1.1
    netmask 255.255.255.0


sudo systemctl restart networking
systemctl status networking.service
```
