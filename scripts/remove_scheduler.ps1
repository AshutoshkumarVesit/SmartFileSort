# SmartFileSort - Remove Scheduled Task
# This PowerShell script removes the SmartFileSort scheduled task

# Check if running as administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))
{
    Write-Host "This script must be run as Administrator. Restarting with elevated privileges..." -ForegroundColor Yellow
    Start-Process PowerShell -Verb RunAs "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`""
    exit
}

$TaskName = "SmartFileSort-AutoOrganizer"

Write-Host "Removing SmartFileSort Scheduled Task..." -ForegroundColor Yellow

try {
    # Check if task exists
    $existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    
    if ($existingTask) {
        # Remove the task
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
        Write-Host "Task '$TaskName' removed successfully!" -ForegroundColor Green
    } else {
        Write-Host "Task '$TaskName' not found." -ForegroundColor Yellow
    }

} catch {
    Write-Host "Error removing scheduled task: $($_.Exception.Message)" -ForegroundColor Red
}

Read-Host "Press Enter to exit"