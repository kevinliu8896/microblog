#!/bin/bash
python3 -m venv venv
pip3 install -r requirements.txt
pip3 install gunicorn pymysql cryptography
pip3 install flask
FLASK_APP=microblog.py
flask db upgrade