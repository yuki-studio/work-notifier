$ErrorActionPreference = "Stop"
$WorkDir = "c:\Notifier"
$PythonPath = "C:\Python314\python.exe"

Write-Host "Re-registering Morning and Evening tasks..."

# Only re-add Morning and Evening
$Tasks = @(
    @{ Name = "Feishu_ClockIn";  Time = "09:30"; Arg = "morning" },
    @{ Name = "Feishu_ClockOut"; Time = "19:30"; Arg = "evening" }
)

foreach ($t in $Tasks) {
    $ArgStr = "src\main.py " + $t.Arg
    $Action = New-ScheduledTaskAction -Execute $PythonPath -Argument $ArgStr -WorkingDirectory $WorkDir
    $Trigger = New-ScheduledTaskTrigger -Daily -At $t.Time
    
    $TaskName = "Notifier_" + $t.Name
    # Clean up old ones just in case
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    
    # Register new
    Register-ScheduledTask -Action $Action -Trigger $Trigger -TaskName $TaskName -Description "Feishu Notifier"
    
    Write-Host "✅ Restored: $TaskName at $($t.Time)"
}

Write-Host "`n🎉 Full Schedule Restored:"
Write-Host "  - 09:30 Morning   [Active]"
Write-Host "  - 12:30 Lunch     [Active]"
Write-Host "  - 19:30 Evening   [Active]"
