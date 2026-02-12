import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from tasks.clockin.workday import WorkdayChecker
import os
import datetime

config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'calendar.json')
checker = WorkdayChecker(config_path)

print(f"Checking for today: {datetime.date.today()}")
is_work = checker.is_workday()
print(f"Is Workday: {is_work}")
