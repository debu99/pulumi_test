#!/bin/bash
sudo apt update
sudo apt install -y nginx
echo "Hello, Web!" > /var/www/html/index.html
sudo systemctl start nginx
