# PowerShell script to run PyInstaller with proper argument handling
param(
    [string[]]$Arguments
)

# Set working directory
cd $PSScriptRoot

# Run PyInstaller
& ".\venv\Scripts\pyinstaller.exe" @Arguments

# Return exit code
exit $LASTEXITCODE
