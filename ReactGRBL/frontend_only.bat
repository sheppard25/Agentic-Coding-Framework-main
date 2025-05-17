@echo off
setlocal enabledelayedexpansion

REM Définir les couleurs pour une meilleure lisibilité
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "RESET=[0m"

echo %BLUE%====================================%RESET%
echo %BLUE%   Démarrage de ReactGRBL Frontend  %RESET%
echo %BLUE%   (Mode développement sans backend) %RESET%
echo %BLUE%====================================%RESET%
echo.

REM Vérifier si Node.js est installé
echo %YELLOW%Vérification de Node.js...%RESET%
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%Node.js n'est pas installé ou n'est pas dans le PATH.%RESET%
    echo %RED%Veuillez installer Node.js 14 ou supérieur.%RESET%
    pause
    exit /b 1
) else (
    echo %GREEN%Node.js est installé.%RESET%
)

REM Vérifier si les dépendances Node.js sont installées
echo %YELLOW%Vérification des dépendances Node.js...%RESET%
if not exist frontend\node_modules (
    echo %YELLOW%Installation des dépendances Node.js...%RESET%
    cd frontend
    npm install
    cd ..
) else (
    echo %GREEN%Les dépendances Node.js sont installées.%RESET%
)

REM Vérifier si le fichier .env existe, sinon le créer
if not exist frontend\.env (
    echo %YELLOW%Création du fichier .env pour forcer le mode développement...%RESET%
    echo NODE_ENV=development > frontend\.env
    echo VITE_DEV_MODE=true >> frontend\.env
) else (
    echo %GREEN%Le fichier .env existe déjà.%RESET%
)

REM Démarrer le frontend
echo.
echo %BLUE%Démarrage du frontend React en mode développement...%RESET%
echo %YELLOW%ATTENTION: Le backend n'est pas démarré, l'application fonctionnera en mode simulation.%RESET%
echo.
start cmd /k "cd frontend && npm run dev"

echo.
echo %GREEN%ReactGRBL Frontend a été lancé en mode développement!%RESET%
echo %GREEN%Le frontend est accessible à l'adresse: http://localhost:5173%RESET%
echo.
echo %YELLOW%Informations importantes:%RESET%
echo %YELLOW%1. L'application fonctionne en mode simulation (sans backend)%RESET%
echo %YELLOW%2. Les fonctionnalités qui nécessitent le backend ne fonctionneront pas réellement%RESET%
echo %YELLOW%3. Pour utiliser l'application avec un vrai contrôleur GRBL, utilisez demarrer_robuste.bat%RESET%
echo.
echo %BLUE%Appuyez sur une touche pour fermer cette fenêtre. Le serveur frontend continuera à s'exécuter.%RESET%
pause > nul
