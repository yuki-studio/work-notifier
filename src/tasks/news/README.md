# 行业资讯推送任务

这是一个基于 RSS Feed 的技术资讯自动推送模块，可以定期获取并推送最新技术动态。

## 目录结构

```
src/tasks/news/              # 资讯推送任务
├── news_main.py            # 推送主入口
├── rss_reader.py           # RSS 阅读器
├── sources.json            # RSS 源配置
└── README.md               # 说明文档

tasks/news/                  # 调试脚本
├── debug_rss.py            # 调试 RSS 读取
└── debug_single_source.py  # 调试单个源
```

## 功能特性

- **多源聚合**：支持配置多个 RSS 源
- **智能过滤**：按时间范围、分类筛选文章
- **热门话题**：自动提取热门关键词
- **定时推送**：支持每日推送设定时间内的文章
- **飞书集成**：通过飞书机器人推送精美卡片消息

## 使用方法

### 运行推送

```bash
# 基础推送（默认获取过去24小时的文章）
python src/tasks/news/news_main.py

# 自定义时间范围（获取过去12小时的文章）
python src/tasks/news/news_main.py --hours-back 12

# 限制文章数量
python src/tasks/news/news_main.py --max-articles 10

# 调整热门话题阈值
python src/tasks/news/news_main.py --min-trending 3
```

### 调试功能

```bash
# 测试 RSS 读取功能
python tasks/news/debug_rss.py

# 测试单个 RSS 源
python tasks/news/debug_single_source.py
```

## 配置说明

### sources.json

RSS 源配置文件，包含三类资讯源：

```json
{
  "tech_blogs": [...],      // 技术博客
  "dev_tools": [...],       // 开发工具
  "ai_llm": [...]           // AI/LLM 相关
}
```

每个源的配置：

| 字段 | 说明 |
|------|------|
| name | 源名称 |
| url | RSS Feed 地址 |
| enabled | 是否启用 |
| category | 分类标签 |

### 环境变量

| 变量名 | 说明 | 必需 |
|--------|------|------|
| FEISHU_WEBHOOK | 飞书机器人 Webhook 地址 | 是 |

### 命令行参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| --hours-back | 24 | 获取过去几小时的文章 |
| --max-articles | 20 | 最多发送几篇文章 |
| --min-trending | 2 | 热门话题最少出现次数 |

## 推荐的 RSS 源

### 技术博客
- 阮一峰的网络日志: https://www.ruanyifeng.com/blog/atom.xml
- 廖雪峰的官方网站: https://www.liaoxuefeng.com/feeds/atom.xml

### 新闻站点
- InfoQ中文: https://www.infoq.cn/feed
- 36Kr: https://www.36kr.com/feed/
- 掘金: https://juejin.cn/feed/

### 开发社区
- Hacker News: https://hnrss.org/frontpage

### AI 相关
- AI 科技大本营: https://www.jiqizhixin.com/rss

## 依赖

需要安装 `feedparser` 库：

```bash
pip install feedparser
```

## 集成到定时任务

### 使用 GitHub Actions

创建 `.github/workflows/news_push.yml`:

```yaml
name: Tech News Push

on:
  schedule:
    - cron: '0 9 * * *'  # 每天北京时间 9:00
  workflow_dispatch:

jobs:
  push-news:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install feedparser requests
      - name: Run news push
        env:
          FEISHU_WEBHOOK: ${{ secrets.FEISHU_WEBHOOK }}
        run: python src/tasks/news/news_main.py --hours-back 24
```

### 使用本地定时任务

Windows 任务计划程序或 Linux cron 都可以配置定时运行。

## 扩展开发

### 添加新的 RSS 源

在 `sources.json` 中添加配置：

```json
{
  "tech_blogs": [
    {
      "name": "你的源名称",
      "url": "https://example.com/feed/",
      "enabled": true,
      "category": "技术动态"
    }
  ]
}
```

### 自定义消息格式

修改 `news_main.py` 中的 `format_articles_for_card()` 函数。