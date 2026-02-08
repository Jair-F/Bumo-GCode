#!/bin/bash

pip3 install -r requirements.txt
pip3 install pre-commit

git config --global --add safe.directory .
git config --global user.name Jair
git config --global user.email jair.fehlauer@gmail.com

pre-commit install
pre-commit run