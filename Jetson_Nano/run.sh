#!/bin/bash
sudo jetson_clocks --fan
sudo systemctl restart nvargus-daemon.service
python3 main.py --onboard 1
