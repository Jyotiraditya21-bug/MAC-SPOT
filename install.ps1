# install.ps1
# Windows installation script for MAC-SPOT

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Installing MAC-SPOT globally on Windows..." -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

$InstallDir = Join-Path $Home ".mac-spot-app"

# Clean up existing installation
if (Test-Path $InstallDir) {
    Write-Host "Updating existing installation..."
    Remove-Item -Recurse -Force $InstallDir
}

# Clone the repository
Write-Host "Cloning MAC-SPOT repository..."
git clone https://github.com/Jyotiraditya21-bug/MAC-SPOT.git $InstallDir
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to clone repository. Make sure git is installed and configured in your PATH."
    exit 1
}

# Change directory
Set-Location $InstallDir

# Create virtual environment
Write-Host "Setting up Python virtual environment..."
python -m venv .venv
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to create python virtual environment. Make sure python is installed and configured in your PATH."
    exit 1
}

# Install dependencies
Write-Host "Installing requirements..."
& .\.venv\Scripts\pip.exe install -q -e .

# Add alias function to PowerShell Profile
Write-Host "Configuring PowerShell profile..."
$ProfileDir = Split-Path -Parent $PROFILE
if (!(Test-Path $ProfileDir)) {
    New-Item -ItemType Directory -Path $ProfileDir -Force | Out-Null
}
if (!(Test-Path $PROFILE)) {
    New-Item -ItemType File -Path $PROFILE -Force | Out-Null
}

$FunctionCode = @"

# MAC-SPOT Aliases
function mac-spot { & '$InstallDir\.venv\Scripts\mac-spot.exe' `$args }
function ms { & '$InstallDir\.venv\Scripts\mac-spot.exe' `$args }
function spot { & '$InstallDir\.venv\Scripts\mac-spot.exe' `$args }
"@

# Append if not already present
$ProfileContent = Get-Content $PROFILE -ErrorAction SilentlyContinue
if ($ProfileContent -notmatch "function mac-spot") {
    Add-Content $PROFILE $FunctionCode
    Write-Host "✔ Added global 'mac-spot', 'ms', and 'spot' functions to your PowerShell profile ($PROFILE)" -ForegroundColor Green
} else {
    Write-Host "✔ Global aliases are already configured in your PowerShell profile" -ForegroundColor Green
}

Write-Host "============================================================" -ForegroundColor Green
Write-Host "  Successfully installed MAC-SPOT!" -ForegroundColor Green
Write-Host "  Please restart your PowerShell session or run:" -ForegroundColor Green
Write-Host "  . `$PROFILE" -ForegroundColor Yellow
Write-Host "  Then run: mac-spot setup" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Green
