import argparse
import json
import os
import random
import sys
from datetime import datetime, timedelta, timezone

# 添加父目录到路径，以便导入 sender
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.sender import FeishuSender
from workday import WorkdayChecker

# Determine paths
TASK_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(TASK_DIR))
CONFIG_DIR = os.path.join(BASE_DIR, 'config')
TASK_CONFIG_DIR = TASK_DIR

def load_json(filename, config_dir):
    path = os.path.join(config_dir, filename)
    if not os.path.exists(path):
        print(f"Config file not found: {path}")
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="Feishu Clockin Reminder")
    parser.add_argument('type', choices=['morning', 'lunch', 'evening'], help="Reminder type")
    parser.add_argument('--force', action='store_true', help="Force send ignoring workday check")
    args = parser.parse_args()

    print(f"Starting clockin {args.type} reminder task...")

    # 1. Load Configs
    calendar_config_path = os.path.join(CONFIG_DIR, 'calendar.json')
    messages = load_json('messages.json', TASK_CONFIG_DIR)
    settings = load_json('setting.json', CONFIG_DIR)

    # 2. Check Workday
    checker = WorkdayChecker(calendar_config_path)
    is_workday = checker.is_workday()
    print(f"Is today workday? {is_workday}")

    if not args.force and not is_workday:
        print("Today is not a workday. Skipping.")
        return

    # 3. Pick Message
    msg_list = messages.get(args.type, [])
    if not msg_list:
        print(f"No messages defined for {args.type}")
        return

    content_text = random.choice(msg_list)
    print(f"Selected message: {content_text}")

    # 4. Send Message
    # Priority: Env Var > Setting File
    webhook = os.environ.get('FEISHU_WEBHOOK') or settings.get('feishu_webhook')

    if not webhook:
        print("Error: Feishu Webhook not found in environment variables or setting.json")
        sys.exit(1)

    sender = FeishuSender(webhook)

    # Construct Card
    title_map = {
        "morning": "☀️ 上班打卡提醒",
        "lunch": "🍱 午餐休息提醒",
        "evening": "🌙 下班打卡提醒"
    }

    # Calculate Beijing Time (UTC+8)
    utc_now = datetime.now(timezone.utc)
    beijing_time = utc_now.astimezone(timezone(timedelta(hours=8)))

    card = {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": title_map.get(args.type, "🔔 提醒")
            },
            "template": "blue"
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": content_text
                }
            },
            {
                "tag": "note",
                "elements": [
                    {
                        "tag": "plain_text",
                        "content": f"发送时间: {beijing_time.strftime('%H:%M:%S')}"
                    }
                ]
            }
        ]
    }

    sender.send(card)

if __name__ == "__main__":
    main()
