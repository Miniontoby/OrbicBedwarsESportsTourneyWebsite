@echo off
call .\.venv\Scripts\activate
call flask --app esportswebsite run %*
pause
