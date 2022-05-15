#!/bin/bash
#Run with non sudo for safety
sudo apt update -y

sudo apt install python3
sudo apt install python3-pip
pip3 install --no-cache-dir -r requirements.txt

sudo apt install tmux
#https://stackoverflow.com/questions/45231292/how-do-i-bring-a-python-scripts-output-to-foreground-background-in-linux

python3 server.py

