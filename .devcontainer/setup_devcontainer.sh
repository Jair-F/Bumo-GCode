#!/bin/bash

pip3 install -r requirements.txt
pip3 install pre-commit

git config --global --add safe.directory .

pre-commit install
pre-commit run