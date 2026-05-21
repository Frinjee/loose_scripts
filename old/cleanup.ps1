# Combined PowerShell Script to Remove Empty Folders from Start Menu, AppData, and C:\ Drive
# Run as Administrator for full functionality

# Define paths for cleanup
$StartMenuPaths = @(
    "$env:ProgramData\Microsoft\Windows\Start Menu\Programs",
    "$env:APPDATA\Microsoft\Windows\Start Menu\Programs"
)

$AppDataPaths = @(
    "$env:APPDATA",           # Roaming (%AppData%)
    "$env:LOCALAPPDATA",      # Local (%LocalAppData%)
    "$env:USERPROFILE\AppData\LocalLow" # LocalLow
)

$DrivePath = "C:\"  # Root of C drive

# Function to remove empty folders
function Remove-EmptyFolders {
    param (
        [string]$Path
    )
    Write-Host "Scanning for empty folders in: $Path"
    
    Get-ChildItem -Path $Path -Directory -Recurse -ErrorAction SilentlyContinue | Where-Object { 
        -not (Get-ChildItem -Path $_.FullName -Recurse -Force -ErrorAction SilentlyContinue) 
    } | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue

    Write-Host "Cleanup completed for: $Path`n"
}

# Execute cleanup for each section
Write-Host "`n==== Start Menu Cleanup ===="
foreach ($Path in $StartMenuPaths) { Remove-EmptyFolders -Path $Path }

Write-Host "`n==== AppData Cleanup ===="
foreach ($Path in $AppDataPaths) { Remove-EmptyFolders -Path $Path }

Write-Host "`n==== C:\ Drive Cleanup ===="
Remove-EmptyFolders -Path $DrivePath

Write-Host "`n✅ Cleanup Completed Successfully! 🚀"
