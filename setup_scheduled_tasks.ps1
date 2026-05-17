<#
.SYNOPSIS
  Register the two daily OLE pipeline scheduled tasks.

.DESCRIPTION
  Creates / updates two Windows scheduled tasks that call pipeline/refresh.py:

    IEPulse-OLE-Ingest-PaidHours    10:45  — 5 min after paid-hours upload (10:40)
    IEPulse-OLE-Ingest-Production   13:05  — 5 min after production upload (13:00)

  Both tasks read BOTH sources (paid_hours + production). The state file +
  date-stitching make it safe to run twice a day:
    - State "since" mark skips files already processed
    - seen_dates seed prevents row duplication
    - _merge_with_existing absorbs any overlap

  Idempotent — re-run this script any time to update timings; existing
  tasks with the same names are replaced.

.NOTES
  - Place this script in the project root (alongside pipeline/, venv/).
  - Run from an ELEVATED PowerShell prompt:
        .\setup_scheduled_tasks.ps1
  - Logon mode: Password — tasks run whether the user is logged on or not.
    You'll be prompted ONCE for your Windows username + password; the
    credential is stored encrypted in Windows Task Scheduler. Re-running
    this script re-prompts (re-using existing tasks would lose the password).
#>

$ErrorActionPreference = "Stop"

# Resolve absolute paths relative to where this script lives.
$Root      = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonExe = Join-Path $Root "venv\Scripts\python.exe"
$RefreshPy = Join-Path $Root "pipeline\refresh.py"

if (-not (Test-Path $PythonExe)) { throw "venv python not found: $PythonExe" }
if (-not (Test-Path $RefreshPy)) { throw "refresh.py not found:    $RefreshPy" }

# Prompt ONCE for the credentials the tasks should run as.
# Use your own Windows login (jabil\4033375). It needs access to the
# network share \\penhomev10\OLE — your own account already does.
Write-Host ""
Write-Host "Enter the Windows credentials the scheduled tasks should run as."
Write-Host "Use your domain login (e.g. jabil\4033375). The password is stored"
Write-Host "encrypted in Windows Task Scheduler — you only type it once."
Write-Host ""
$cred = Get-Credential -Message "Credentials for the OLE scheduled tasks"
$plainPwd = $cred.GetNetworkCredential().Password

function Register-OleTask {
    param(
        [string]$Name,
        [string]$Time,
        [string]$Description
    )

    $action = New-ScheduledTaskAction `
        -Execute $PythonExe `
        -Argument "`"$RefreshPy`"" `
        -WorkingDirectory $Root

    $trigger = New-ScheduledTaskTrigger -Daily -At $Time

    # StartWhenAvailable      : run on next login if machine was off at trigger time
    # DontStopOnIdleEnd       : don't stop mid-run if machine becomes idle
    # MultipleInstances=IgnoreNew : if previous still running, skip this trigger
    # ExecutionTimeLimit=30m  : kill after 30 min (full refresh should finish in <1 min)
    $settings = New-ScheduledTaskSettingsSet `
        -StartWhenAvailable `
        -DontStopOnIdleEnd `
        -ExecutionTimeLimit (New-TimeSpan -Minutes 30) `
        -MultipleInstances IgnoreNew

    if (Get-ScheduledTask -TaskName $Name -ErrorAction SilentlyContinue) {
        Unregister-ScheduledTask -TaskName $Name -Confirm:$false
        Write-Host "Replaced existing: $Name"
    }

    # Password logon: task runs whether the user is logged on or not.
    Register-ScheduledTask `
        -TaskName $Name `
        -Description $Description `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -User $cred.UserName `
        -Password $plainPwd `
        -RunLevel Highest | Out-Null

    Write-Host "Registered: $Name at $Time daily"
}

Register-OleTask `
    -Name "IEPulse-OLE-Ingest-PaidHours" `
    -Time "10:45" `
    -Description "Daily OLE pipeline refresh after paid hours upload."

Register-OleTask `
    -Name "IEPulse-OLE-Ingest-Production" `
    -Time "13:05" `
    -Description "Daily OLE pipeline refresh after production upload."

Write-Host ""
Write-Host "Done. Useful commands:"
Write-Host "  Get-ScheduledTask -TaskName 'IEPulse-OLE-*'"
Write-Host "  Start-ScheduledTask -TaskName 'IEPulse-OLE-Ingest-PaidHours'    # manual test run"
Write-Host "  Get-ScheduledTaskInfo -TaskName 'IEPulse-OLE-Ingest-PaidHours'  # last run result"

