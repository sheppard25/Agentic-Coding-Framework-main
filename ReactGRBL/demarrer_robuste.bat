@echo off
setlocal enabledelayedexpansion

REM Définir les couleurs pour une meilleure lisibilité
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "RESET=[0m"

echo %BLUE%====================================%RESET%
echo %BLUE%   Démarrage de ReactGRBL Controller%RESET%
echo %BLUE%====================================%RESET%
echo.

REM Définir le port du backend (par défaut 8000)
set BACKEND_PORT=8000

REM Vérifier si le port 8000 est déjà utilisé
echo %YELLOW%Vérification du port %BACKEND_PORT%...%RESET%
netstat -ano | findstr :%BACKEND_PORT% > nul
if %errorlevel% equ 0 (
    echo %YELLOW%Le port %BACKEND_PORT% est déjà utilisé. Tentative avec le port 8001...%RESET%
    set BACKEND_PORT=8001
    
    REM Vérifier si le port 8001 est déjà utilisé
    netstat -ano | findstr :%BACKEND_PORT% > nul
    if %errorlevel% equ 0 (
        echo %YELLOW%Le port %BACKEND_PORT% est déjà utilisé. Tentative avec le port 8002...%RESET%
        set BACKEND_PORT=8002
        
        REM Vérifier si le port 8002 est déjà utilisé
        netstat -ano | findstr :%BACKEND_PORT% > nul
        if %errorlevel% equ 0 (
            echo %RED%Tous les ports testés sont déjà utilisés. Veuillez libérer un port et réessayer.%RESET%
            pause
            exit /b 1
        )
    )
)

echo %GREEN%Utilisation du port %BACKEND_PORT% pour le backend.%RESET%

REM Vérifier si Python est installé
echo %YELLOW%Vérification de Python...%RESET%
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%Python n'est pas installé ou n'est pas dans le PATH.%RESET%
    echo %RED%Veuillez installer Python 3.8 ou supérieur.%RESET%
    pause
    exit /b 1
) else (
    echo %GREEN%Python est installé.%RESET%
)

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

REM Vérifier si les dépendances Python sont installées
echo %YELLOW%Vérification des dépendances Python...%RESET%
cd backend
python -c "import fastapi" >nul 2>&1
if %errorlevel% neq 0 (
    echo %YELLOW%Installation de FastAPI...%RESET%
    pip install fastapi
)

python -c "import uvicorn" >nul 2>&1
if %errorlevel% neq 0 (
    echo %YELLOW%Installation de Uvicorn...%RESET%
    pip install uvicorn
)

python -c "import serial" >nul 2>&1
if %errorlevel% neq 0 (
    echo %YELLOW%Installation de PySerial...%RESET%
    pip install pyserial
)

echo %GREEN%Toutes les dépendances Python sont installées.%RESET%
cd ..

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

REM Modifier le fichier App.jsx pour utiliser le bon port
echo %YELLOW%Configuration du frontend pour utiliser le port %BACKEND_PORT%...%RESET%
powershell -Command "(Get-Content frontend\src\App.jsx) -replace 'http://localhost:8000', 'http://localhost:%BACKEND_PORT%' | Set-Content frontend\src\App.jsx"

REM Démarrer le backend
echo.
echo %BLUE%Démarrage du backend Python sur le port %BACKEND_PORT%...%RESET%
start cmd /k "cd backend && python -m uvicorn app.main:app --reload --host 127.0.0.1 --port %BACKEND_PORT%"

REM Attendre que le backend démarre
echo %YELLOW%Attente du démarrage du backend (15 secondes)...%RESET%
timeout /t 15 /nobreak > nul

REM Vérifier si le backend est accessible
echo %YELLOW%Vérification de l'accès au backend...%RESET%
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:%BACKEND_PORT%' -UseBasicParsing -TimeoutSec 5; Write-Host '%GREEN%Backend accessible!%RESET%' } catch { Write-Host '%RED%ATTENTION: Le backend ne semble pas accessible!%RESET%'; }"

REM Démarrer le frontend
echo.
echo %BLUE%Démarrage du frontend React...%RESET%
start cmd /k "cd frontend && npm run dev"

echo.
echo %GREEN%ReactGRBL Controller a été lancé!%RESET%
echo %GREEN%Le backend est accessible à l'adresse: http://localhost:%BACKEND_PORT%%RESET%
echo %GREEN%Le frontend est accessible à l'adresse: http://localhost:5173%RESET%
echo.
echo %YELLOW%Si vous rencontrez des problèmes de connexion:%RESET%
echo %YELLOW%1. Exécutez le script diagnostic.bat pour vérifier l'état du système%RESET%
echo %YELLOW%2. Vérifiez que le backend est bien en cours d'exécution%RESET%
echo %YELLOW%3. Vérifiez qu'aucun autre processus n'utilise le port %BACKEND_PORT%%RESET%
echo %YELLOW%4. Redémarrez l'application si nécessaire%RESET%
echo.
echo %BLUE%Appuyez sur une touche pour fermer cette fenêtre. Les serveurs continueront à s'exécuter.%RESET%
pause > nul
