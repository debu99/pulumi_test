#!/bin/bash
sudo apt update
sudo apt install -y nodejs npm
sudo npm install http-server -g
echo "Hello, API!" > index.html
nohup http-server -p 80 &