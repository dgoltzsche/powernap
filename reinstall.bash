#!/bin/bash
sudo systemctl disable powernapd
sudo systemctl stop powernapd
./uninstall.bash
makepkg -f 
./install.bash
sudo systemctl daemon-reload
sudo systemctl enable powernapd
sudo systemctl start powernapd
journalctl -xe