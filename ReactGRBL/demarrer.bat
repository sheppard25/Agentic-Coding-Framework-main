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
python -c "import fastapi, uvicorn, serial" >nul 2>&1
if %errorlevel% neq 0 (
    echo %YELLOW%Installation des dépendances Python...%RESET%
    pip install fastapi uvicorn pyserial
) else (
    echo %GREEN%Les dépendances Python sont installées.%RESET%
)
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

REM Démarrer le backend avec une vérification robuste
echo.
echo %BLUE%Démarrage du backend Python...%RESET%

REM Tuer tout processus existant sur le port 8000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    echo %YELLOW%Arrêt du processus existant sur le port 8000 (PID: %%a)...%RESET%
    taskkill /F /PID %%a >nul 2>&1
)

REM Démarrer le backend dans une nouvelle fenêtre
start cmd /k "cd backend && python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

REM Attendre que le backend démarre
echo %YELLOW%Attente du démarrage du backend (10 secondes)...%RESET%
timeout /t 10 /nobreak > nul

REM Vérifier si le backend est accessible
echo %YELLOW%Vérification de l'accès au backend...%RESET%
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000' -UseBasicParsing -TimeoutSec 5; if ($response.StatusCode -eq 200) { Write-Host '%GREEN%Backend accessible!%RESET%' } } catch { Write-Host '%RED%ATTENTION: Le backend ne semble pas accessible!%RESET%'; Write-Host '%YELLOW%Tentative de redémarrage du backend...%RESET%'; }"

REM Démarrer le frontend
echo.
echo %BLUE%Démarrage du frontend React...%RESET%
start cmd /k "cd frontend && npm run dev"

echo.
echo %GREEN%ReactGRBL Controller a été lancé!%RESET%
echo %GREEN%Le backend est accessible à l'adresse: http://localhost:8000%RESET%
echo %GREEN%Le frontend est accessible à l'adresse: http://localhost:5173%RESET%
echo.
echo %YELLOW%Si vous rencontrez des problèmes de connexion:%RESET%
echo %YELLOW%1. Vérifiez que le backend est bien en cours d'exécution%RESET%
echo %YELLOW%2. Vérifiez qu'aucun autre processus n'utilise le port 8000%RESET%
echo %YELLOW%3. Redémarrez l'application si nécessaire%RESET%
echo.
echo %BLUE%Appuyez sur une touche pour fermer cette fenêtre. Les serveurs continueront à s'exécuter.%RESET%
pause > nul
