#!/bin/bash

python -m nuitka --jobs=$(nproc) --standalone \
    --onefile --mingw64 --lto=no --assume-yes-for-downloads \
    --windows-console-mode=attach \
    --include-data-dir=data=data --include-data-files=icon/icon.ico=icon/icon.ico \
    --onefile-windows-splash-screen-image=data/splash.png \
    --windows-icon-from-ico=icon/icon.ico \
    --company-name="Koeger" --product-name="Bumo-GCode" \
    --file-version=x.x.x --product-version=x.x.x \
    --file-description="Copier" --copyright="2026" \
    --output-filename=app.exe src/app.py


# --user-package-configuration-file=nuitka-package.config.yml \
# python -m nuitka --windows-console-mode=attach --jobs=16 --standalone --onefile --mingw64 --lto=no --assume-yes-for-downloads --include-data-dir=data=data --include-data-files=icon/icon.ico=icon/icon.ico --onefile-windows-splash-screen-image=data/splash.png --windows-icon-from-ico=icon/icon.ico --company-name="Koeger" --product-name="Bumo-GCode" --file-version=0.0.0 --product-version=0.0.0 --file-description="Bumo-GCode Copier" --copyright="2026" --output-filename=app.exe src/app.py
