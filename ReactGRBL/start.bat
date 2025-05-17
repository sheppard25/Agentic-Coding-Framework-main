@echo off
echo ===================================
echo Demarrage de ReactGRBL Controller
echo ===================================
echo.

REM Verifier si Python est installe
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python n'est pas installe ou n'est pas dans le PATH.
    echo Veuillez installer Python 3.8 ou superieur.
    pause
    exit /b 1
)

REM Verifier si Node.js est installe
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Node.js n'est pas installe ou n'est pas dans le PATH.
    echo Veuillez installer Node.js 14 ou superieur.
    pause
    exit /b 1
)

echo Demarrage du backend Python...
start cmd /k "cd backend && python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

echo Attente du démarrage du backend (5 secondes)...
timeout /t 5 /nobreak > nul

echo Demarrage du frontend React...
start cmd /k "cd frontend && npm run dev"

echo.
echo ReactGRBL Controller a ete lance avec succes!
echo Le backend est accessible a l'adresse: http://localhost:8000
echo Le frontend est accessible a l'adresse: http://localhost:5173
echo.
echo Appuyez sur une touche pour fermer cette fenetre. Les serveurs continueront a s'executer.
pause > nul
