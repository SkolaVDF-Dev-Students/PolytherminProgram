@echo off
setlocal

REM ============================
REM  CONFIG
REM ============================
set DEVELOPER_MODE=true
set DIST_DIR=dist

echo --------------------------------------
echo    Welcome to the build script (Win)
echo --------------------------------------

REM ============================
REM  CHECK / INSTALL MPREMOTE
REM ============================
if "%DEVELOPER_MODE%"=="false" (
    echo [INFO] Kontroluji mpremote...

    where mpremote >nul 2>nul
    if errorlevel 1 (
        echo [INFO] mpremote nenalezen – instaluji...
        pip install mpremote
        if errorlevel 1 (
            echo [ERROR] Instalace mpremote selhala.
            exit /b 1
        )
    ) else (
        echo [INFO] mpremote OK
    )
) else (
    echo [DEV MODE] Přeskakuji kontrolu mpremote.
)

REM ============================
REM  PREPARE DIST
REM ============================
echo [INFO] Čistím a vytvářím složku %DIST_DIR%...
rmdir /s /q %DIST_DIR% 2>nul
mkdir %DIST_DIR%

echo [INFO] Kopíruji main.py a libs...
copy main.py %DIST_DIR% >nul
xcopy libs %DIST_DIR%\libs /E /I /Y >nul

REM ============================
REM  VERSIONING
REM ============================
if "%DEVELOPER_MODE%"=="true" (
    echo [DEV MODE] Zapisuji verzi: dev
    echo dev > %DIST_DIR%\version.txt
) else (
    set /p VERSION=Zadej verzi buildu (napr. 1.0.0): 
    echo [INFO] Verze: %VERSION%
    echo %VERSION% > %DIST_DIR%\version.txt
)

REM ============================
REM  CREATE ZIP (ONLY OFFICIAL)
REM ============================
if "%DEVELOPER_MODE%"=="false" (
    echo [INFO] Vytvářím dist.zip...
    powershell -command "Compress-Archive -Path '%DIST_DIR%\*' -DestinationPath 'dist.zip' -Force"
)

REM ============================
REM  RUN MPREMOTE
REM ============================
cd %DIST_DIR%

echo [INFO] Upload přes mpremote...
python -m mpremote connect auto fs cp -r . :

echo [INFO] Hotovo!
