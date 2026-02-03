import requests
import datetime

date_str = "2026-02-03"
url = f"http://timor.tech/api/holiday/info/{date_str}"

try:
    print(f"Checking API for {date_str}...")
    resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
    print(f"Status Code: {resp.status_code}")
    print(f"Response: {resp.text}")
except Exception as e:
    print(f"Error: {e}")
