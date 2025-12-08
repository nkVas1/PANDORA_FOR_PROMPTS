@echo off
REM Build PANDORA executable with PyInstaller
REM This batch script properly handles long command lines on Windows

cd /d "%~dp0"

REM Clean old builds
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
for %%F in (*.spec) do del /q "%%F"

REM Run PyInstaller with all necessary flags
echo Building PANDORA Desktop Application...
echo.

venv\Scripts\pyinstaller.exe --onedir --noconfirm --clean --paths backend --add-data "backend;backend" --add-data "frontend;frontend" --add-data "data;data" --add-data "references;references" --add-data "frontend\pandora.db;frontend" --hidden-import=app --hidden-import=fastapi --hidden-import=uvicorn --hidden-import=sqlalchemy --hidden-import=pydantic --hidden-import=aiosqlite --hidden-import=webview --collect-all=fastapi --collect-all=uvicorn --collect-all=sqlalchemy --collect-all=pydantic --collect-all=webview --collect-submodules=app --name PANDORA launcher_final.py

echo.
echo Checking build...
if exist dist\PANDORA\PANDORA.exe (
  echo Build successful!
  echo Executable: dist\PANDORA\PANDORA.exe
  REM Get file size
  for %%A in (dist\PANDORA\PANDORA.exe) do (
    set /a size=%%~zA / 1048576
    echo Size: !size! MB
  )
) else (
  echo Build failed - executable not found
  exit /b 1
)
