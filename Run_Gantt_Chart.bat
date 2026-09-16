@echo off
title Gantt Chart App Launcher
echo Starting the Gantt Chart Application...
set STREAMLIT_PATH="C:\Users\manmo\AppData\Local\Python\pythoncore-3.14-64\Scripts\streamlit.exe"
cd /d "%~dp0"
%STREAMLIT_PATH% run gantt_app.py
pause
