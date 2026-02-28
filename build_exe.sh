#!/bin/bash

wine python -m nuitka --standalone --onefile --jobs=$(nproc) \
    --assume-yes-for-downloads \
    --windows-icon-from-ico=icon/icon.ico \
    --windows-console-mode=disable \
    --mingw64 --lto=no --remove-output \
    --onefile-windows-splash-screen-image=data/splash.png \
    src/app.py -o app.exe

# python -m nuitka --standalone --user-package-configuration-file=my-package.nuitka-package.config.yml main.py

# --onefile-no-compression
# --onefile-windows-splash-screen-image=data/splash.png

: <<'COMMENT'
linux:
python3 -m pip install patchelf
python3 -m nuitka --standalone --onefile --jobs=$(nproc) \
    --assume-yes-for-downloads \
    --windows-icon-from-ico=icon/icon.ico \
    --windows-console-mode=disable \
    --mingw64 --lto=no --remove-output \
    src/app.py -o app.exe
COMMENT
