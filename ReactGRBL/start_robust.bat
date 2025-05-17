@echo off
echo ===================================
echo Demarrage de ReactGRBL Controller
echo ===================================
echo.

REM Définir les couleurs pour les messages
set "RED=PowerShell Write-Host -ForegroundColor Red"
set "GREEN=PowerShell Write-Host -ForegroundColor Green"
set "YELLOW=PowerShell Write-Host -ForegroundColor Yellow"

REM Vérifier si Python est installé
echo Verification de Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    %RED% "Python n'est pas installe ou n'est pas dans le PATH."
    %RED% "Veuillez installer Python 3.8 ou superieur."
    pause
    exit /b 1
) else (
    %GREEN% "Python est installe."
)

REM Vérifier si Node.js est installé
echo Verification de Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    %RED% "Node.js n'est pas installe ou n'est pas dans le PATH."
    %RED% "Veuillez installer Node.js 14 ou superieur."
    pause
    exit /b 1
) else (
    %GREEN% "Node.js est installe."
)

REM Vérifier si les ports sont déjà utilisés
echo Verification des ports...
netstat -ano | findstr :8000 >nul
if %errorlevel% equ 0 (
    %YELLOW% "ATTENTION: Le port 8000 est deja utilise."
    %YELLOW% "Le backend pourrait ne pas demarrer correctement."
    %YELLOW% "Voulez-vous continuer quand meme? (O/N)"
    set /p choice=
    if /i "%choice%" neq "O" exit /b 1
)

netstat -ano | findstr :5173 >nul
if %errorlevel% equ 0 (
    %YELLOW% "ATTENTION: Le port 5173 est deja utilise."
    %YELLOW% "Le frontend pourrait ne pas demarrer correctement."
    %YELLOW% "Voulez-vous continuer quand meme? (O/N)"
    set /p choice=
    if /i "%choice%" neq "O" exit /b 1
)

REM Vérifier si les dépendances sont installées
echo Verification des dependances du backend...
if not exist "backend\venv" (
    %YELLOW% "L'environnement virtuel Python n'existe pas. Creation..."
    cd backend
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
    cd ..
) else (
    %GREEN% "L'environnement virtuel Python existe."
)

echo Verification des dependances du frontend...
if not exist "frontend\node_modules" (
    %YELLOW% "Les modules Node.js ne sont pas installes. Installation..."
    cd frontend
    npm install
    cd ..
) else (
    %GREEN% "Les modules Node.js sont installes."
)

REM Démarrer le backend
echo.
%GREEN% "Demarrage du backend Python..."
start cmd /k "cd backend && python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

REM Attendre que le backend démarre
echo Attente du demarrage du backend (5 secondes)...
timeout /t 5 /nobreak > nul

REM Vérifier si le backend est accessible
echo Verification de l'acces au backend...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000/status' -UseBasicParsing; if ($response.StatusCode -eq 200) { Write-Host 'Backend accessible!' -ForegroundColor Green } } catch { Write-Host 'ATTENTION: Le backend ne semble pas accessible!' -ForegroundColor Red }"

REM Démarrer le frontend
echo.
%GREEN% "Demarrage du frontend React..."
start cmd /k "cd frontend && npm run dev"

echo.
%GREEN% "ReactGRBL Controller a ete lance!"
%GREEN% "Le backend est accessible a l'adresse: http://localhost:8000"
%GREEN% "Le frontend est accessible a l'adresse: http://localhost:5173"
echo.
echo Appuyez sur une touche pour fermer cette fenetre. Les serveurs continueront a s'executer.
pause > nul
