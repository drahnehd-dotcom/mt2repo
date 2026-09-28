@echo off
setlocal
cd /d "%~dp0"
if "%~1"=="" (
  set /p "INPUT=Unpacked folder: "
) else set "INPUT=%~1"
where py >nul 2>nul
if %errorlevel%==0 (set "PY=py") else (
  set "PY=python"
)
%PY% -m pip install -r "%~dp0requirements.txt"
if errorlevel 1 (pause & exit /b 1)
%PY% "%~dp0zarc_v4.py" pack "%INPUT%"
echo.
pause
endlocal
