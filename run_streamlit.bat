@echo off
cd /d "%~dp0"
set PYTHONPATH=%CD%\venv\Lib\site-packages;%PYTHONPATH%
.\venv\Scripts\python.exe -m streamlit run Home.py %*
pause
