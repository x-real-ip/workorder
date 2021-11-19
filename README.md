# installation

## 1. install python

```bash
sudo apt update
sudo apt -y upgrade
```

check if python is installed

```
python3 -V
```

install pip

```
sudo apt install -y python3-pip
```

setting Up a Virtual Environment

```
sudo apt install -y python3-venv
mkdir environments
cd environments
```

create an environment

```
python3 -m venv workorder
```

use the environment

```
source workorder/bin/activate

```

install package

```
pip3 install selenium
```

## 2. install Google Chrome 

```
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
```

```
sudo apt install ./google-chrome-stable_current_amd64.deb
```
