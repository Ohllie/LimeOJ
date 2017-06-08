#!/bin/bash

source /lime-code/venv/bin/activate
cd /lime-code/lime/app
python3 manage.py db upgrade
