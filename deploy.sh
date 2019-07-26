git fetch origin
git pull origin master
sudo apt update && sudo apt upgrade
sudo apt install python3-venv
/usr/bin/python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python3 server.py
