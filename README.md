Installation:

Python extension,

Ev3 extension,
https://marketplace.visualstudio.com/items?itemName=ev3dev.ev3dev-browser

```cmd
python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install --upgrade python-ev3dev2
pip install --upgrade pyusb
pip install --upgrade opencv-python

------ to deactivate
deactivate
```

SSH onto ev3: default user: `robot`, pw: `maker`

```cmd
ssh -o PasswordAuthentication=yes -o PreferredAuthentications=keyboard-interactive,password -o PubkeyAuthentication=no robot@10.42.0.3
ssh -o PasswordAuthentication=yes -o PreferredAuthentications=keyboard-interactive,password -o PubkeyAuthentication=no robot@10.42.0.4
```
