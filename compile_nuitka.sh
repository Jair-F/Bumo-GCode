#!/bin/bash

# Docker: kniwase/wine-python-nuitka:3.10

# --experimental=new-dll-tool \
# --windows-console-mode=disable \
# --lto=no

wine python -m pip install -r requirements.txt
wine python -m nuitka --standalone --onefile --jobs=$(nproc) \
    --assume-yes-for-downloads \
    --onefile-no-compression \
    --windows-icon-from-ico=icon/icon.ico \
    --mingw64 --lto=no --remove-output \
    src/app.py -o app_uncompressed.exe

wine python -m nuitka --standalone --onefile --jobs=$(nproc) \
    --assume-yes-for-downloads \
    --windows-icon-from-ico=icon/icon.ico \
    --mingw64 --lto=no --remove-output \
    --windows-console-mode=disable \
    src/app.py -o app_compressed.exe

# --report
# --remove-output --assume-yes-for-downloads
# faster - no compression: --onefile-no-compression
# --onefile-windows-splash-screen-image=data/splash.png  \
