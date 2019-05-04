#!/usr/bin/env bash

cd site;
python3 manage.py makemigrations && python3 manage.py migrate;
python3 manage.py runserver
