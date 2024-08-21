install:

Python extension,

Ev3 extension,
https://marketplace.visualstudio.com/items?itemName=ev3dev.ev3dev-browser

```cmd
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install --upgrade python-ev3dev2
pip install --upgrade nxt-python
pip install --upgrade pyusb
pip install --upgrade ev3_dc # not working, just test
pip install --upgrade opencv-python


------ to deactivate
deactivate
```

SSH onto ev3: default user: `robot`, pw: `maker`

```cmd
ssh -o PasswordAuthentication=yes -o PreferredAuthentications=keyboard-interactive,password -o PubkeyAuthentication=no robot@10.42.0.235
```

Update and upgrade stuff:

```cmd
sudo nano /etc/apt/sources.list

------ replace first with second:
deb http://httpredir.debian.org/debian stretch main contrib non-free
#deb-src http://httpredir.debian.org/debian stretch main contrib non-free
deb http://security.debian.org/ stretch/updates main contrib non-free
#deb-src http://security.debian.org/ stretch/updates main contrib non-free


deb http://archive.debian.org/debian/ stretch main contrib non-free
#deb-src http://archive.debian.org/debian/ stretch main contrib non-free
deb http://archive.debian.org/debian-security/ stretch/updates main contrib non-free
#deb-src http://archive.debian.org/debian-security/ stretch/updates main contrib non-free
------

sudo apt-get update
```

activate the right python interpreter (lower right)

Hardware: Install ev3dev https://www.ev3dev.org/
Connection to network over usb tutorial: https://www.ev3dev.org/docs/tutorials/connecting-to-the-internet-via-usb/

Control the nxt over USB (latest version of the package):

https://github.com/schodet/nxt-python

Outdated installer for Installing the nxt-slave package on the ev3: https://github.com/ev3dev/nxt-python

This will take AGES, because the ev3 is really slow

```cmd
sudo apt install build-essential checkinstall \
libreadline-gplv2-dev libncursesw5-dev libssl-dev \
libsqlite3-dev tk-dev libgdbm-dev libc6-dev \
libbz2-dev libffi-dev zlib1g-dev

sudo apt install software-properties-common

cd /usr/src
sudo wget https://www.python.org/ftp/python/3.8.0/Python-3.8.0.tgz
sudo tar xzf Python-3.8.0.tgz
cd Python-3.8.0

sudo ./configure --enable-optimizations
sudo make altinstall
```

<!-- ```cmd
sudo apt install python3-usb
sudo apt install python3-pip
# python3 -m pip install --upgrade nxt-python
python3 -m pip install --ignore-requires-python --no-dependencies --upgrade -v https://files.pythonhosted.org/packages/e5/b0/7f312509cafe9d0a51b63c8e98b628eac30c127f1c97b299b4653e534066/nxt_python-3.3.0-py3-none-any.whl
``` -->
<!-- ```cmd
wget https://github.com/ev3dev/nxt-python/archive/refs/tags/ev3dev-stretch/3.0_20180424.1.9851bee-1ev3dev1.zip
unzip 3.0_20180424.1.9851bee-1ev3dev1.zip
cd nxt-python-ev3dev-stretch-3.0_20180424.1.9851bee-1ev3dev1/
sudo python3 setup.py install
``` -->
