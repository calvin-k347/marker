$tailwind = Get-CimInstance Win32_Process | Where-Object {
    $_.CommandLine -like "*tailwindcss*" -and $_.CommandLine -like "*--watch*"
}

if (-not $tailwind) {
    Start-Process -WindowStyle hidden "cmd.exe" -ArgumentList '/c', 'npx @tailwindcss/cli -i ./static/styles/input.css -o ./static/styles/output.css --watch'
}
