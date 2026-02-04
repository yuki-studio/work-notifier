$ErrorActionPreference = "Stop"
$WorkDir = "c:\Notifier"
$PythonPath = "C:\Python314\python.exe"

Write-Host "Python: $PythonPath"
Write-Host "WorkDir: $WorkDir"

$Tasks = @(
    @{ Name = "Feishu_ClockIn";  Time = "09:30"; Arg = "morning" },
    @{ Name = "Feishu_Lunch";    Time = "12:30"; Arg = "lunch" },
    @{ Name = "Feishu_ClockOut"; Time = "19:30"; Arg = "evening" }
)

foreach ($t in $Tasks) {
    $ArgStr = "src\main.py " + $t.Arg
    $Action = New-ScheduledTaskAction -Execute $PythonPath -Argument $ArgStr -WorkingDirectory $WorkDir
    $Trigger = New-ScheduledTaskTrigger -Daily -At $t.Time
    
    $TaskName = "Notifier_" + $t.Name
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Register-ScheduledTask -Action $Action -Trigger $Trigger -TaskName $TaskName -Description "Feishu Notifier"
    
    Write-Host "✅ Registered: $TaskName at $($t.Time)"
}
