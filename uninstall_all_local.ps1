# Remove ALL local notifier tasks to avoid duplication with Supabase
$ErrorActionPreference = "Stop"

$TasksToRemove = @(
    "Notifier_Feishu_ClockIn",
    "Notifier_Feishu_Lunch", 
    "Notifier_Feishu_ClockOut"
)

Write-Host "🧹 Cleaning up local scheduled tasks..."

foreach ($TaskName in $TasksToRemove) {
    try {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction Stop
        Write-Host "✅ Successfully removed: $TaskName"
    } catch {
        # Check if error is "Task not found"
        if ($_.Exception.Message -like "*No MSFT_ScheduledTask objects found*") {
            Write-Host "ℹ️ Task not found (already clean): $TaskName"
        } else {
            Write-Host "ℹ️ Task not found or already clean: $TaskName"
        }
    }
}

Write-Host "`n🎉 All local tasks cleared! Your bot is now 100% Cloud-Native on Supabase."
