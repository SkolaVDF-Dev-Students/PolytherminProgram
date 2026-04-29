@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM ============================
REM  CONFIG
REM ============================
set DEVELOPER_MODE=true
set DIST_DIR=dist

echo --------------------------------------
echo    Welcome to the build script (Win)
echo --------------------------------------

REM ============================
REM  PREPARE DIST
REM ============================
echo [INFO] Cistim a vytvarim slozku %DIST_DIR%...
if exist "%DIST_DIR%" rmdir /s /q "%DIST_DIR%"
mkdir "%DIST_DIR%"

echo [INFO] Kopiruji main.py a libs...
if not exist "main.py" (
    echo [ERROR] Soubor main.py nebyl nalezen.
    exit /b 1
)

if not exist "libs" (
    echo [ERROR] Slozka libs nebyla nalezena.
    exit /b 1
)

copy /Y "main.py" "%DIST_DIR%\" >nul
if errorlevel 1 (
    echo [ERROR] Nepodarilo se zkopirovat main.py
    exit /b 1
)

xcopy "libs" "%DIST_DIR%\libs" /E /I /Y >nul
if errorlevel 1 (
    echo [ERROR] Nepodarilo se zkopirovat libs
    exit /b 1
)

REM ============================
REM  VERSIONING
REM ============================
if /I "%DEVELOPER_MODE%"=="true" (
    echo [DEV MODE] Zapisuji verzi: dev
    > "%DIST_DIR%\version.txt" echo dev
) else (
    set /p VERSION=Zadej verzi buildu ^(napr. 1.0.0^): 
    echo [INFO] Verze: !VERSION!
    > "%DIST_DIR%\version.txt" echo !VERSION!
)

REM ============================
REM  CREATE ZIP (ONLY OFFICIAL)
REM ============================
if /I "%DEVELOPER_MODE%"=="false" (
    echo [INFO] Vytvarim dist.zip...
    if exist "dist.zip" del /f /q "dist.zip"
    powershell -NoProfile -Command "Compress-Archive -Path '%DIST_DIR%\*' -DestinationPath 'dist.zip' -Force"
    if errorlevel 1 (
        echo [ERROR] Nepodarilo se vytvorit dist.zip
        exit /b 1
    )
)

REM ============================
REM  RUN MPREMOTE
REM ============================
echo [INFO] Upload pres mpremote...
mpremote connect auto fs cp -r "%DIST_DIR%\." :
if errorlevel 1 (
    echo [ERROR] Upload pres mpremote selhal.
    exit /b 1
)

echo [INFO] Hotovo!
exit /b 0