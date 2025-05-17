@echo off
setlocal enabledelayedexpansion

echo ===================================
echo Arrêt de ReactGRBL Controller
echo ===================================
echo.

echo Recherche des processus Python (backend)...
for /f "tokens=2" %%a in ('tasklist ^| findstr python') do (
    echo Arrêt du processus Python (PID: %%a)...
    taskkill /F /PID %%a >nul 2>&1
)

echo Recherche des processus Node.js (frontend)...
for /f "tokens=2" %%a in ('tasklist ^| findstr node') do (
    echo Arrêt du processus Node.js (PID: %%a)...
    taskkill /F /PID %%a >nul 2>&1
)

echo Vérification des ports 8000, 8001 et 8002...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    echo Arrêt du processus sur le port 8000 (PID: %%a)...
    taskkill /F /PID %%a >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8001') do (
    echo Arrêt du processus sur le port 8001 (PID: %%a)...
    taskkill /F /PID %%a >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8002') do (
    echo Arrêt du processus sur le port 8002 (PID: %%a)...
    taskkill /F /PID %%a >nul 2>&1
)

echo Vérification du port 5173 (frontend)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5173') do (
    echo Arrêt du processus sur le port 5173 (PID: %%a)...
    taskkill /F /PID %%a >nul 2>&1
)

echo.
echo ===================================
echo ReactGRBL Controller a été arrêté
echo ===================================

pause
