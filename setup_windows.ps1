# PolicyBot Windows PowerShell Setup Script
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " PolicyBot - Windows Setup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# Step 1
Write-Host "`n[1/4] Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv
& .\venv\Scripts\Activate.ps1

# Step 2
Write-Host "[2/4] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Step 3 - install dependencies
Write-Host "[3/4] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Step 4 - ingest documents
Write-Host "[4/4] Building local index..." -ForegroundColor Yellow
python rag\ingest.py

Write-Host "`n============================================" -ForegroundColor Green
Write-Host " Done! Run the app with:  python app.py" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
