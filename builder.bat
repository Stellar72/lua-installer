@echo off
pyinstaller --onefile --icon="logo.ico" main.py
xcopy /y "dist\main.exe"
rd /s /q "dist"
rd /s /q "build"
del main.spec
