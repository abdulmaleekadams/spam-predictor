#!/bin/bash

python -m venv venv

source ./venv/Scripts/activate

pip install -r ./requirements.txt

echo "Package installed successfully"

fastapi dev main.py

start http://127.0.0.1:8000
