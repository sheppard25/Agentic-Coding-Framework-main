@echo off
setlocal enabledelayedexpansion

echo ===================================
echo Diagnostic ReactGRBL
echo ===================================
echo.

echo Verification des ports utilises...
netstat -ano | findstr :8000
echo.

echo Verification des processus Python en cours...
tasklist | findstr python
echo.

echo Verification des versions installees...
echo Python:
python --version
echo.
echo Node.js:
node --version
echo.
echo NPM:
npm --version
echo.

echo Verification des dependances Python...
echo.
python -c "import sys; print('Python Path:'); print('\n'.join(sys.path))"
echo.
python -c "import sys; print('Installed Packages:'); import pkg_resources; print('\n'.join([p.project_name for p in pkg_resources.working_set]))"
echo.

echo Verification de l'acces au backend...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000' -UseBasicParsing -TimeoutSec 2; Write-Host 'Backend accessible: ' $response.StatusCode } catch { Write-Host 'Backend non accessible: ' $_.Exception.Message }"
echo.

echo Verification de l'acces au frontend...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:5173' -UseBasicParsing -TimeoutSec 2; Write-Host 'Frontend accessible: ' $response.StatusCode } catch { Write-Host 'Frontend non accessible: ' $_.Exception.Message }"
echo.

echo ===================================
echo Diagnostic termine
echo ===================================

pause
