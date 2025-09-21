# SmartFileSort - Windows Task Scheduler Setup Script
# This PowerShell script creates a scheduled task to run SmartFileSort automatically

# Check if running as administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))
{
    Write-Host "This script must be run as Administrator. Restarting with elevated privileges..." -ForegroundColor Yellow
    Start-Process PowerShell -Verb RunAs "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`""
    exit
}

Write-Host "Setting up SmartFileSort Scheduled Task..." -ForegroundColor Green

# Configuration
$TaskName = "SmartFileSort-AutoOrganizer"
$Description = "Automatically organizes files using SmartFileSort tool"
$ScriptPath = Join-Path $PSScriptRoot "run_organizer.bat"
$WorkingDirectory = Split-Path $PSScriptRoot -Parent

# Check if script exists
if (-not (Test-Path $ScriptPath)) {
    Write-Host "Error: Batch script not found at $ScriptPath" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

try {
    # Remove existing task if it exists
    $existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($existingTask) {
        Write-Host "Removing existing task..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    }

    # Create action
    $Action = New-ScheduledTaskAction -Execute $ScriptPath -WorkingDirectory $WorkingDirectory

    # Create trigger (runs every hour)
    $Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 1)

    # Create settings
    $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable:$false

    # Create principal (run as current user)
    $Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType ServiceAccount

    # Register the task
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Description $Description

    Write-Host "Task '$TaskName' created successfully!" -ForegroundColor Green
    Write-Host "The task will run every hour starting now." -ForegroundColor Green
    
    # Show task information
    Write-Host "`nTask Details:" -ForegroundColor Cyan
    Write-Host "  Name: $TaskName"
    Write-Host "  Script: $ScriptPath"
    Write-Host "  Schedule: Every hour"
    Write-Host "  User: $env:USERNAME"
    
    Write-Host "`nTo manage the task, use:" -ForegroundColor Yellow
    Write-Host "  - Task Scheduler (taskschd.msc)"
    Write-Host "  - PowerShell: Get-ScheduledTask -TaskName '$TaskName'"
    
    # Ask if user wants to run the task now
    $runNow = Read-Host "`nWould you like to run the task now to test it? (y/N)"
    if ($runNow -eq 'y' -or $runNow -eq 'Y') {
        Write-Host "Starting task..." -ForegroundColor Green
        Start-ScheduledTask -TaskName $TaskName
        Write-Host "Task started. Check the logs in the 'logs' directory for results." -ForegroundColor Green
    }

} catch {
    Write-Host "Error creating scheduled task: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "`nSetup complete!" -ForegroundColor Green
Read-Host "Press Enter to exit"