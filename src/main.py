import argparse
import json
import os
import random
import sys
from datetime import datetime
from workday import WorkdayChecker
from sender import FeishuSender

# Determine paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, 'config')

def load_json(filename):
    path = os.path.join(CONFIG_DIR, filename)
    if not os.path.exists(path):
        print(f"Config file not found: {path}")
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="Feishu Reminder Bot")
    parser.add_argument('type', choices=['morning', 'lunch', 'evening'], help="Reminder type")
    parser.add_argument('--force', action='store_true', help="Force send ignoring workday check")
    args = parser.parse_args()

    print(f"Starting {args.type} reminder task...")

    # 1. Load Configs
    calendar_config_path = os.path.join(CONFIG_DIR, 'calendar.json')
    messages = load_json('messages.json')
    settings = load_json('setting.json')
    
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
        # Don't fail hard if testing locally without config, just warn
        sys.exit(1)
        
    sender = FeishuSender(webhook)
    
    # Construct Card
    title_map = {
        "morning": "☀️ 上班打卡提醒",
        "lunch": "🍱 午餐休息提醒",
        "evening": "🌙 下班打卡提醒"
    }
    
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
                        "content": f"发送时间: {datetime.now().strftime('%H:%M:%S')}"
                    }
                ]
            }
        ]
    }
    
    sender.send(card)

if __name__ == "__main__":
    main()
