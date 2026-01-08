@echo off
powershell -Command "git stash"
powershell -Command "git pull origin main"
chcp 65001 > nul
start "" "obsidian://open?vault=Курс школьной физики"
exit