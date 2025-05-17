@echo off
echo ===================================
echo    Demarrage de ReactGRBL Controller
echo ===================================
echo.

REM Verifier si Python est installe
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python n'est pas installe ou n'est pas dans le PATH.
    echo Veuillez installer Python 3.8+ et reessayer.
    goto :error
)

REM Verifier si Node.js est installe
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Node.js n'est pas installe ou n'est pas dans le PATH.
    echo Veuillez installer Node.js v14+ et reessayer.
    goto :error
)

echo Verification des dependances...

REM Creer le repertoire data s'il n'existe pas
if not exist "backend\data" mkdir "backend\data"
if not exist "backend\data\files" mkdir "backend\data\files"

REM Installer les dependances Python si necessaire
echo Installation des dependances Python...
if exist "backend\requirements.txt" (
    pip install -r backend\requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo Erreur lors de l'installation des dependances Python.
        goto :error
    )
) else (
    echo Fichier requirements.txt non trouve dans le dossier backend.
    goto :error
)

REM Installer les dependances Node.js si necessaire
echo Installation des dependances Node.js...
if exist "frontend\package.json" (
    cd frontend
    call npm install
    if %ERRORLEVEL% NEQ 0 (
        echo Erreur lors de l'installation des dependances Node.js.
        cd ..
        goto :error
    )
    cd ..
) else (
    echo Fichier package.json non trouve dans le dossier frontend.
    goto :error
)

echo.
echo Toutes les dependances sont installees.
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

goto :end

:error
echo.
echo Une erreur s'est produite lors du demarrage de l'application.
echo Veuillez verifier les messages d'erreur ci-dessus.
pause
exit /b 1

:end
echo.
echo Appuyez sur une touche pour fermer cette fenetre...
pause >nul
