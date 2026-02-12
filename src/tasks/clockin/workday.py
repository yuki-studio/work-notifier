import datetime
import json
import os
import requests

class WorkdayChecker:
    def __init__(self, config_path):
        self.config = self._load_config(config_path)
        
    def _load_config(self, path):
        if not os.path.exists(path):
            print(f"Warning: Config file not found at {path}")
            return {"holidays": [], "makeup_workdays": []}
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def is_workday(self, date_obj=None):
        """
        判断指定日期是否为工作日
        优先使用在线 API，失败时回退到本地配置
        :param date_obj: datetime.date 对象，默认为今天
        :return: Boolean
        """
        if date_obj is None:
            date_obj = datetime.date.today()
        
        date_str = date_obj.strftime('%Y-%m-%d')
        
        # 尝试使用在线 API (timor.tech)
        # API 文档: https://timor.tech/api/holiday
        # type: 0=工作日, 1=假日, 2=节日, 3=调休(要上班)
        # 简化版接口: http://timor.tech/api/holiday/info/$date
        # 只要 type.type 是 0 或 3，就是工作日
        
        try:
            url = f"http://timor.tech/api/holiday/info/{date_str}"
            # 设置短超时，避免阻塞太久
            resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('code') == 0:
                    day_type = data['type']['type']
                    # 0: 工作日, 3: 调休后补班 --> 这两种情况要上班
                    is_work = (day_type == 0 or day_type == 3)
                    print(f"[API] Date: {date_str}, Type: {day_type}, IsWorkday: {is_work}")
                    return is_work
        except Exception as e:
            print(f"[API Error] Failed to fetch holiday info: {e}. Fallback to local config.")

        # --- Fallback: 本地兜底逻辑 ---
        
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
