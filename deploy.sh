#!/usr/bin/env bash
files=(config lollibot util lollibot.py)

echo "Uploading files"

scp -rp ${files[@]} robot@ev3dev.local:~/

echo "Setting the current date to $(date)"

ssh robot@ev3dev.local "echo maker | sudo -kS date -s '$(date)'"

echo "Run lollibot.py on Brickman to start the application"
