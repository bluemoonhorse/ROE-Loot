@echo off
cd /d "%~dp0"
py -3 roe_loot_editor.py
if errorlevel 1 pause
