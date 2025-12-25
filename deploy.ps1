# ================= CONFIG =================
$ProjectDir = "D:\SourceCode\agents\tro_ly\"
$PythonExe  = "python"   # hoặc full path tới python trong venv
$App        = "app.main:app"

$Args = "-m uvicorn $App --host 0.0.0.0  --port 1116"

$StdOutLog  = "$ProjectDir\logs\uvicorn.normal.log"
$StdErrLog  = "$ProjectDir\logs\uvicorn.important.log"

# ================= MOVE TO PROJECT =================
Set-Location $ProjectDir

.\stop.ps1

# ================= START NEW UVICORN =================
Start-Process `
    -FilePath $PythonExe `
    -ArgumentList $Args `
    -WindowStyle Hidden `
    -RedirectStandardOutput $StdOutLog `
    -RedirectStandardError  $StdErrLog
