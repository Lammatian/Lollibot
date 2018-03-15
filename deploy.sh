#!/usr/bin/env bash
files=(config lollibot util lollibot.py)

echo "Uploading files"

scp -rp ${files[@]} robot@ev3dev.local:~/

echo "Run lollibot.py on Brickman to start the application"