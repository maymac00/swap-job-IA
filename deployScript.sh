#!/bin/bash
sudo apt update -y

sudo apt install python3 python3-pip
pip install --no-cache-dir -r requirements.txt

python3 server.py