@echo off
set "project_dir=%USERPROFILE%\Desktop\ironhackData\week7\chess_dataset"

cd "%project_dir%"

REM Run the Python scripts with full paths
python "%project_dir%\pgn_to_csv.py"
python "%project_dir%\main.py"

pause

