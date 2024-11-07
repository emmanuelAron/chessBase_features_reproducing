@echo off
REM Define a variable for the base path
set "base_dir=%USERPROFILE%\Desktop\ironhackData\week7"

REM Use the base variable to define the project path
set "project_dir=%base_dir%\chess_dataset"

REM Navigate to the project directory
cd "%project_dir%"

REM Run the Python scripts
python pgn_to_csv.py
python main.py

pause

