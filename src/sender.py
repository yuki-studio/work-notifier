import requests
import json
import sys

class FeishuSender:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send(self, content):
        """
        发送飞书消息
        :param content: 消息内容。如果是字符串，发送普通文本；如果是字典，发送富文本卡片。
        """
        if not self.webhook_url:
            print("Error: Webhook URL is not configured.")
            return False
            
        payload = {}
        if isinstance(content, dict):
            # 认为是卡片消息 (Interactive)
            payload = {
                "msg_type": "interactive",
                "card": content
            }
        else:
            # 认为是普通文本 (Text)
            payload = {
                "msg_type": "text",
                "content": {
                    "text": str(content)
                }
            }
            
        try:
            import time
            headers = {"Content-Type": "application/json"}
            
            # Retry logic: 3 times, wait 5s between retries
            max_retries = 3
            for i in range(max_retries):
                try:
                    response = requests.post(self.webhook_url, headers=headers, json=payload, timeout=10)
                    response.raise_for_status()
                    result = response.json()
                    
                    if result.get("code") == 0:
                        print(f"Message sent successfully: {content if isinstance(content, str) else 'Card'}")
                        return True
                    else:
                        print(f"Feishu API returned error: {result}")
                        return False
                except requests.exceptions.RequestException as e:
                    print(f"Attempt {i+1}/{max_retries} failed: {e}")
                    if i < max_retries - 1:
                        time.sleep(5)
                    else:
                        print("All retry attempts failed.")
                        return False
                
        except Exception as e:
            print(f"Exception occurred while sending message: {e}")
            return False
