#!/bin/sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd website
python main.py
