@echo off
echo Installing Claude Beeper...

set DEST=%ProgramFiles%\ClaudeBeeper
mkdir "%DEST%" 2>nul
copy /Y dist\ClaudeBeeper.exe "%DEST%\ClaudeBeeper.exe"

echo Adding to Windows startup...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" ^
    /v "ClaudeBeeper" ^
    /t REG_SZ ^
    /d "\"%DEST%\ClaudeBeeper.exe\"" ^
    /f

echo Done. Claude Beeper is installed and will start with Windows.
echo Location: %DEST%\ClaudeBeeper.exe
pause