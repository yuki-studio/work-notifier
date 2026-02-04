$ErrorActionPreference = "Stop"

# 1. Unregister Morning and Evening tasks
$TasksToRemove = @("Notifier_Feishu_ClockIn", "Notifier_Feishu_ClockOut")

foreach ($TaskName in $TasksToRemove) {
    try {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction Stop
        Write-Host "✅ Successfully removed task: $TaskName"
    } catch {
        Write-Host "ℹ️ Task not found or already removed: $TaskName"
    }
}

Write-Host "`n🎉 Adjustment Complete!"
Write-Host "Current Status:"
Write-Host "  - Morning Reminder: [Disabled]"
Write-Host "  - Lunch Reminder:   [Active] (Remains unchanged)"
Write-Host "  - Evening Reminder: [Disabled]"
