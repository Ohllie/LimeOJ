#!/bin/bash

source /lime-code/venv/bin/activate

echo "Starting lime"

# kill existing app.py, hacky but who cares
ps x | grep "python3.*app/app.py" | grep -v grep | awk '{print $1}' | xargs kill -9

# launch the app
exec python3 /lime-code/lime/app/app.py