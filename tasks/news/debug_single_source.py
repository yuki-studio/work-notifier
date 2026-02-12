import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import feedparser

# 测试单个 RSS 源
def test_single_source(url):
    print(f"Testing RSS source: {url}")
    print("=" * 50)

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        feed = feedparser.parse(url, agent=headers['User-Agent'])

        print(f"Feed title: {feed.feed.get('title', 'N/A')}")
        print(f"Feed description: {feed.feed.get('description', 'N/A')[:100]}...")
        print(f"Number of entries: {len(feed.entries)}")

        if feed.bozo:
            print(f"\n⚠️ Warning: Feed may be malformed")
            print(f"Bozo exception: {feed.bozo_exception}")

        print("\nFirst 5 entries:")
        print("=" * 50)

        for i, entry in enumerate(feed.entries[:5], 1):
            print(f"\n{i}. {entry.get('title', 'N/A')}")
            print(f"   Link: {entry.get('link', 'N/A')}")
            print(f"   Published: {entry.get('published', 'N/A')}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

# 测试几个常用源
if __name__ == "__main__":
    test_sources = [
        "https://www.ruanyifeng.com/blog/atom.xml",
        "https://hnrss.org/frontpage",
        "https://juejin.cn/feed/",
    ]

    for url in test_sources:
        print("\n" + "=" * 50)
        test_single_source(url)