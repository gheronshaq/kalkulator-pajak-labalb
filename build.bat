@echo off
echo ================================================
echo  Kalkulator Pajak LABALB - Build Script
echo ================================================
echo.

echo [1/4] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo [2/4] Cleaning previous build...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo.

echo [3/4] Building executable with PyInstaller...
pyinstaller build_config.spec
if %errorlevel% neq 0 (
    echo Error: Build failed
    pause
    exit /b 1
)
echo.

echo [4/4] Cleaning up temporary files...
if exist build rmdir /s /q build
echo.

echo ================================================
echo  Build completed successfully!
echo  Executable location: dist\KalkulatorPajakLABALB.exe
echo ================================================
echo.
pause
