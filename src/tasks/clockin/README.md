# 打卡提醒任务

这是 Notifier 工程中处理打卡提醒的模块。

## 目录结构

```
src/
└── tasks/
    └── clockin/          # 打卡提醒任务
        ├── main.py       # 打卡任务入口
        ├── workday.py    # 工作日检查器
        ├── messages.json # 打卡消息模板
        └── README.md     # 说明文档

tasks/
└── clockin/             # 打卡任务调试脚本
    ├── debug_api.py     # 调试 API 请求
    └── debug_workday_now.py # 调试工作日检查
```

## 使用方法

### 运行打卡提醒

```bash
# 上班打卡提醒
python src/tasks/clockin/main.py morning

# 午餐休息提醒
python src/tasks/clockin/main.py lunch

# 下班打卡提醒
python src/tasks/clockin/main.py evening

# 强制发送（跳过工作日检查）
python src/tasks/clockin/main.py morning --force
```

### 调试功能

```bash
# 检查 API 是否正常工作
python tasks/clockin/debug_api.py

# 检查今天是否为工作日
python tasks/clockin/debug_workday_now.py
```

## 配置文件

- **calendar.json** - 存储法定节假日和调休补班信息
- **setting.json** - 存储飞书 webhook URL
- **messages.json** - 存储各时段的提醒消息模板

## 依赖

- 需要安装 `requests` 库
- 飞书 webhook URL 可通过环境变量 `FEISHU_WEBHOOK` 或配置文件设置

## 自定义消息

编辑 `messages.json` 文件来自定义不同时段的提醒消息。

每个时段支持多条消息，程序会随机选择一条发送。

## 开发说明

该模块支持：
- 工作日检查（API + 本地配置双重保障）
- 重试机制（3次尝试，每次间隔5秒）
- 时区处理（使用北京时间）
- 支持强制发送模式