#!/bin/bash

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source ./venv/Scripts/activate

# Install required packages
pip install -r ./requirements.txt

echo "Packages installed successfully"

# Run the FastAPI server in the background
uvicorn main:app --reload &

# Wait for the server to start
sleep 3

# Open the index.html in the default web browser

if which xdg-open > /dev/null
then
  xdg-open http://127.0.0.1:8000
elif which gnome-open > /dev/null
then
  gnome-open http://127.0.0.1:8000
elif which open > /dev/null
then
  open http://127.0.0.1:8000
else
start http://127.0.0.1:8000
fi

wait
