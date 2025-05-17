@echo off
echo ===================================
echo    Demarrage de ReactGRBL Controller
echo ===================================
echo.

REM Demarrer le backend dans une nouvelle fenetre
echo Demarrage du backend Python...
start cmd /k "cd backend && python run.py"

REM Attendre que le backend demarre
echo Attente du demarrage du backend (5 secondes)...
timeout /t 5 /nobreak >nul

REM Demarrer le frontend dans une nouvelle fenetre
echo Demarrage du frontend React...
start cmd /k "cd frontend && npm run dev"

echo.
echo ===================================
echo ReactGRBL Controller est en cours d'execution!
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Pour arreter l'application, fermez les fenetres de terminal.
echo ===================================

echo.
echo Appuyez sur une touche pour fermer cette fenetre...
pause >nul
