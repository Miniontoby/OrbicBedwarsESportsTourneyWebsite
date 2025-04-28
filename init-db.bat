@echo off
call .\.venv\Scripts\activate
call flask --app esportswebsite init-db %*
pause
