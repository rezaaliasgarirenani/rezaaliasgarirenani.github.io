param(
    [ValidateRange(1024, 65535)]
    [int]$Port = 8000
)

# Serve this repository even when the script is called from a different folder.
Write-Host "Preview: http://127.0.0.1:$Port/"
Write-Host 'Press Ctrl+C to stop.'
python -m http.server $Port --bind 127.0.0.1 --directory $PSScriptRoot
