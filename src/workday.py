import datetime
import json
import os

class WorkdayChecker:
    def __init__(self, config_path):
        self.config = self._load_config(config_path)
        
    def _load_config(self, path):
        if not os.path.exists(path):
            # Fallback or log warning
            print(f"Warning: Config file not found at {path}")
            return {"holidays": [], "makeup_workdays": []}
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def is_workday(self, date_obj=None):
        """
        判断指定日期是否为工作日
        :param date_obj: datetime.date 对象，默认为今天
        :return: Boolean
        """
        if date_obj is None:
            date_obj = datetime.date.today()
        
        date_str = date_obj.strftime('%Y-%m-%d')
        
        # 1. 优先判断法定节假日 (Holidays)
        if date_str in self.config.get('holidays', []):
            return False
            
        # 2. 其次判断调休补班 (Make-up Workdays)
        if date_str in self.config.get('makeup_workdays', []):
            return True
            
        # 3. 最后判断周末 (Saturday=5, Sunday=6)
        if date_obj.weekday() >= 5:
            return False
            
        return True
