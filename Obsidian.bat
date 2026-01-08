@echo off
powershell -Command "git stash"
powershell -Command "git pull origin main"
call run.bat
exit