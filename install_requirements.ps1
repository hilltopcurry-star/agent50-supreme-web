# install_requirements.ps1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = "C:\Users\ADMIN\Desktop\agent 50"
Write-Host "Running automated installer in: $root"

Push-Location $root

# Ensure venv exists
if (-Not (Test-Path ".\.venv\Scripts\Activate")) {
    Write-Host "ERROR: .venv not found. Create or activate your venv first." -ForegroundColor Red
    Pop-Location
    exit 1
}

# Activate venv
Write-Host "Activating .venv..."
& .\.venv\Scripts\Activate

# Show python
$py = & python -c "import sys; print(sys.version.split()[0]); print(sys.executable)"
Write-Host "Using Python:" $py

# Upgrade pip tooling
Write-Host "`nUpgrading pip, setuptools, wheel, build..."
python -m pip install --upgrade pip setuptools wheel build | Out-Host

# List of packages
$pkgs = @("numpy","scipy","flask","sqlalchemy","requests","jinja2","PyJWT","pillow","opencv-python")

# ***** FIX: initialize failed array *****
$failed = @()

# Install packages
foreach ($pkg in $pkgs) {
    try {
        Write-Host "`nInstalling $pkg (prefer-binary)..."
        python -m pip install --prefer-binary $pkg --progress-bar off | Out-Host
        Write-Host "$pkg installed" -ForegroundColor Green
    } catch {
        Write-Host "Warning: $pkg failed first attempt, retrying..." -ForegroundColor Yellow
        try {
            python -m pip install $pkg --progress-bar off | Out-Host
            Write-Host "$pkg installed on retry" -ForegroundColor Green
        } catch {
            Write-Host "ERROR: $pkg could not be installed." -ForegroundColor Red
            $failed += $pkg
        }
    }
}

# Installed status
Write-Host "`n=== Installed status ==="
foreach ($pkg in $pkgs) {
    Write-Host "`nChecking $pkg..."
    python -m pip show $pkg | Out-Host
}

# Failed packages
if ($failed.Count -gt 0) {
    Write-Host "`nSome packages failed: $failed" -ForegroundColor Red
    Write-Host "If you see build errors (cl / msvc), install Visual C++ Build Tools:"
    Write-Host "https://visualstudio.microsoft.com/visual-cpp-build-tools/"
} else {
    Write-Host "`nAll packages installed successfully." -ForegroundColor Green
}

# Run fix_installation.py
Write-Host "`nRunning fix_installation.py for final check..."
python fix_installation.py

Pop-Location
