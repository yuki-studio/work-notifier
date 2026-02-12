import argparse
import json
import os
import random
import sys
from datetime import datetime, timedelta, timezone

# 添加父目录到路径，以便导入 sender
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.sender import FeishuSender
from rss_reader import RSSReader

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

def format_articles_for_card(articles, max_display=10):
    """将文章格式化为飞书卡片消息"""
    elements = []

    # 添加标题
    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": f"## 📰 今日技术资讯 ({len(articles)}条)\n\n"
        }
    })

    # 限制显示数量
    displayed_articles = articles[:max_display]

    for i, article in enumerate(displayed_articles, 1):
        # 文章标题
        elements.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"### {i}. {article['title']}\n"
            }
        })

        # 来源和分类
        elements.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"📌 来源：{article['source_name']} | 分类：{article['category']}\n"
            }
        })

        # 摘要
        if article['summary']:
            summary = article['summary'][:200] + '...' if len(article['summary']) > 200 else article['summary']
            elements.append({
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"{summary}\n"
                }
            })

        # 链接
        elements.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"🔗 [查看原文]({article['link']})\n"
            }
        })

        elements.append({
            "tag": "hr"
        })

    # 添加统计信息
    elements.append({
        "tag": "note",
        "elements": [
            {
                "tag": "plain_text",
                "content": f"生成时间: {datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')}"
            }
        ]
    })

    return elements

def generate_greeting():
    """生成问候语"""
    greetings = [
        "早上好，为您奉上最新的技术资讯！",
        "早安，看看今天有什么新发现？",
        "新的一天，新的技术动态！",
        "早！今天的技术新鲜货已送达~"
    ]
    return random.choice(greetings)

def generate_hot_topics(topics):
    """生成热门话题模块"""
    if not topics:
        return []

    elements = [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"\n\n## 🔥 热门话题\n"
            }
        }
    ]

    for i, topic in enumerate(topics[:5], 1):
        elements.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"{i}. #{topic}\n"
            }
        })

    return elements

def main():
    parser = argparse.ArgumentParser(description="Tech News Push")
    parser.add_argument('--hours-back', type=int, default=24,
                       help="Hours back to fetch articles (default: 24)")
    parser.add_argument('--max-articles', type=int, default=20,
                       help="Maximum articles to send (default: 20)")
    parser.add_argument('--min-trending', type=int, default=2,
                       help="Minimum articles for trending topic (default: 2)")
    args = parser.parse_args()

    print(f"Starting tech news push...")

    # 1. Load Configs
    settings = load_json('setting.json', CONFIG_DIR)

    # 2. Create RSS Reader
    sources_file = os.path.join(TASK_CONFIG_DIR, 'sources.json')
    if not os.path.exists(sources_file):
        print(f"Error: Sources file not found at {sources_file}")
        sys.exit(1)

    rss_reader = RSSReader(sources_file)

    # 3. Fetch Articles
    print(f"Fetching articles from last {args.hours_back} hours...")
    articles = rss_reader.fetch_all_articles(
        max_articles_per_source=5,
        hours_back=args.hours_back
    )

    if not articles:
        print("No articles found.")
        return

    print(f"Found {len(articles)} articles")

    # 4. Get Hot Topics
    hot_topics = rss_reader.get_trending_topics(articles, args.min_trending)

    # 5. Create Card
    card = {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": "📰 技术资讯推送"
            },
            "template": "yellow"
        },
        "elements": []
    }

    # 添加问候语
    card["elements"].append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": f"## {generate_greeting()}\n\n"
        }
    })

    # 添加文章列表
    card["elements"].extend(format_articles_for_card(articles, args.max_articles))

    # 添加热门话题
    if hot_topics:
        card["elements"].extend(generate_hot_topics(hot_topics))

    # 6. Send Message
    # Priority: Env Var > Setting File
    webhook = os.environ.get('FEISHU_WEBHOOK') or settings.get('feishu_webhook')

    if not webhook:
        print("Error: Feishu Webhook not found in environment variables or setting.json")
        sys.exit(1)

    sender = FeishuSender(webhook)
    sender.send(card)

    print(f"Sent {len(articles)} articles successfully!")

if __name__ == "__main__":
    main()