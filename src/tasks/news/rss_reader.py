import feedparser
import requests
from datetime import datetime, timedelta
import time
from urllib.parse import urlparse
import re

class RSSReader:
    def __init__(self, sources_file):
        self.sources = self._load_sources(sources_file)

    def _load_sources(self, sources_file):
        """加载 RSS 源配置"""
        try:
            import json
            import os
            with open(sources_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading sources: {e}")
            return {}

    def fetch_all_articles(self, max_articles_per_source=5, hours_back=24):
        """获取所有启用的源的文章"""
        all_articles = []

        for category, sources in self.sources.items():
            for source in sources:
                if not source.get('enabled', False):
                    continue

                try:
                    print(f"Fetching from {source['name']}...")
                    articles = self._fetch_from_source(
                        source['url'],
                        source['name'],
                        max_articles_per_source,
                        hours_back
                    )
                    all_articles.extend(articles)
                except Exception as e:
                    print(f"Error fetching from {source['name']}: {e}")
                    continue

        # 按时间排序，最新的在前
        all_articles.sort(key=lambda x: x['published'], reverse=True)
        return all_articles

    def _fetch_from_source(self, url, source_name, max_articles, hours_back):
        """从单个源获取文章"""
        try:
            # 设置 User-Agent 避免被拒绝
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            # 解析 RSS Feed
            feed = feedparser.parse(url, agent=headers['User-Agent'])

            if feed.bozo:
                print(f"Warning: Feed may be malformed for {source_name}")

            articles = []
            now = datetime.now()
            cutoff_time = now - timedelta(hours=hours_back)

            for entry in feed.entries[:max_articles]:
                # 解析发布时间
                published = self._parse_datetime(entry.get('published_parsed', entry.get('updated_parsed')))

                if published and published < cutoff_time:
                    continue

                article = {
                    'title': entry.get('title', '无标题'),
                    'link': entry.get('link', ''),
                    'summary': entry.get('summary', ''),
                    'published': published,
                    'source_name': source_name,
                    'category': self._get_category(source_name),
                    'description': self._clean_html(entry.get('description', ''))
                }

                articles.append(article)

            return articles

        except Exception as e:
            print(f"Error fetching from {url}: {e}")
            return []

    def _parse_datetime(self, parsed_time):
        """解析时间为 datetime 对象"""
        if not parsed_time:
            return None
        try:
            return datetime(*parsed_time[:6])
        except:
            return None

    def _get_category(self, source_name):
        """根据源名获取分类"""
        for category, sources in self.sources.items():
            for source in sources:
                if source['name'] == source_name:
                    return source.get('category', '其他')
        return '其他'

    def _clean_html(self, html_text):
        """清理 HTML 标签"""
        if not html_text:
            return ''

        # 简单的 HTML 清理
        clean = re.compile('<.*?>')
        return re.sub(clean, '', html_text).strip()

    def get_trending_topics(self, articles, min_articles=2):
        """获取热门话题（简单实现：出现次数最多的关键词）"""
        word_count = {}

        for article in articles:
            # 简单分词
            words = re.findall(r'[\w\u4e00-\u9fa5]+', article['title'])

            for word in words:
                if len(word) > 1:  # 过滤单字符
                    word_count[word] = word_count.get(word, 0) + 1

        # 返回出现次数最多的词
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        return [word for word, count in sorted_words if count >= min_articles]