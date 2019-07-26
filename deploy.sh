git fetch origin
git pull origin master
sudo apt update && sudo apt upgrade
sudo apt install python3-venv
python3 -m venv env
source env/bin/activate
pip install -r requirements.py
/usr/bin/tmux kill-session -t prod
/usr/bin/tmux new -s prod -d python3 server.py
