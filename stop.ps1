$PORT = 1116


$connections = Get-NetTCPConnection -LocalPort $PORT -State Listen -ErrorAction SilentlyContinue

if (-not $connections) {
    Write-Host "No process is listening on port $PORT. Nothing to stop."
    exit 0
}

foreach ($conn in $connections) {
    $processId = $conn.OwningProcess

    if ($processId -and (Get-Process -Id $processId -ErrorAction SilentlyContinue)) {
        Stop-Process -Id $processId -Force
        Write-Host "Stopped process PID $processId on port $PORT"
    }
}