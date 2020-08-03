#!/bin/bash
echo "Hello, World!" > index.html
nohup python3 -m http.server 80 &
