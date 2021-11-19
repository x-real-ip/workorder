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

## 2. install selenium python package

```
pip3 install selenium
```

## 3. install google-chrome
```
sudo apt update
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
```

wget https://chromedriver.storage.googleapis.com/96.0.4664.45/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver
```

## 4. install chromium webdriver

```
sudo apt-get update -y
sudo apt-get install -y chromium-chromedriver
```

