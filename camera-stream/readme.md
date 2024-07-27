# Flashing and Pre-requesites

https://randomnerdtutorials.com/video-streaming-with-raspberry-pi-camera/

When Flashing the os, make sure to `enable ssh` and set password to `pi`

# Web streaming example

Source code from the official PiCamera package

http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming

Paste script

```
nano rpi_camera_stream.py
```

Enable Camera Support

```
sudo raspi-config
```

-   Interface Options
-   Legacy Camera support
-   Enable
-   RESTART

Install packages

```
sudo apt install python3-picamera
export PATH="/home/pi/.local/lib/python3.9/site-packages:$PATH"
sudo python3 rpi_camera_surveillance_system.py
```

# Make it its own wlan-server

```
sudo apt install dnsmasq hostapd iptables
```

```cmd
sudo nano /etc/dhcpcd.conf

>>>>>

interface wlan0
static ip_address=192.168.1.1/24
nohook wpa_supplicant
```

```cmd
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf_alt
sudo nano /etc/dnsmasq.conf

>>>>>

# DHCP-Server aktiv für WLAN-Interface
interface=wlan0
# DHCP-Server nicht aktiv für bestehendes Netzwerk
no-dhcp-interface=eth0
# IPv4-Adressbereich und Lease-Time
dhcp-range=192.168.1.100,192.168.1.200,255.255.255.0,24h
# DNS
dhcp-option=option:dns-server,192.168.1.1
```

```cmd
sudo nano /etc/hostapd/hostapd.conf

>>>>>

# WLAN-Router-Betrieb
# Schnittstelle und Treiber
interface=wlan0
#driver=nl80211
# WLAN-Konfiguration
ssid=WLANrouter
channel=1
hw_mode=g
ieee80211n=1
ieee80211d=1
country_code=DE
wmm_enabled=1
# WLAN-Verschlüsselung
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_passphrase=testtest
```

```cmd
sudo nano /etc/default/hostapd

>>>>>

RUN_DAEMON=yes
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```

```cmd
sudo systemctl unmask hostapd
sudo systemctl start hostapd
sudo systemctl enable hostapd
```
