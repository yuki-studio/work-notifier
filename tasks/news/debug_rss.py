import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from tasks.news.rss_reader import RSSReader

# 获取 sources.json 路径
sources_file = os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'tasks', 'news', 'sources.json')

print("Testing RSS Reader...")
print(f"Sources file: {sources_file}")
print("=" * 50)

try:
    reader = RSSReader(sources_file)

    print("\nFetching articles (last 24 hours)...")
    articles = reader.fetch_all_articles(
        max_articles_per_source=3,
        hours_back=24
    )

    print(f"\nFound {len(articles)} articles:")
    print("=" * 50)

    for i, article in enumerate(articles, 1):
        print(f"\n{i}. {article['title']}")
        print(f"   来源: {article['source_name']}")
        print(f"   分类: {article['category']}")
        print(f"   发布时间: {article['published']}")
        print(f"   链接: {article['link']}")
        if article['summary']:
            print(f"   摘要: {article['summary'][:100]}...")

    # 获取热门话题
    print("\n" + "=" * 50)
    print("Trending topics:")
    topics = reader.get_trending_topics(articles, min_articles=2)
    for topic in topics:
        print(f"  - #{topic}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()