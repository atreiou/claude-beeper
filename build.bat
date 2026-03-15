@echo off
echo Generating icon...
python create_icon.py

echo Building executable...
pyinstaller --onefile --windowed --icon=icon.ico --name=ClaudeBeeper claude_beeper.py

echo Done. Executable is in the dist\ folder.
pause