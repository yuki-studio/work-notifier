# 飞书工作日常定时提醒 (Feishu Reminder Bot)

基于 GitHub Actions 的飞书定时提醒机器人，覆盖上下班打卡与午餐订餐场景。

## 功能

* ⏰ **定时触发**：每天 09:30, 12:30, 19:00 自动运行。
* 📅 **工作日判断**：自动跳过节假日与周末，支持补班配置。
* 🎲 **随机文案**：每次推送不同文案，拒绝枯燥。
* 🤖 **消息推送**：支持飞书 Webhook 富文本卡片消息。

## 快速开始

### 1. Fork 本仓库
点击右上角 Fork 按钮。

### 2. 配置飞书 Webhook
1. 在飞书群组中添加「自定义机器人」。
2. 获取 Webhook URL (例如 `https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx`).
3. 在 GitHub 仓库 Settings -> Secrets and variables -> Actions 中添加 Secret:
   * Name: `FEISHU_WEBHOOK`
   * Value: 你的 Webhook URL

### 3. 启用 GitHub Actions
进入 Actions 页面，允许 Workflow 运行。

## 配置说明

* `config/messages.json`: 修改提醒文案。
* `config/calendar.json`: 配置节假日与补班。

## 本地运行

```bash
pip install -r requirements.txt
# Windows Powershell
$env:FEISHU_WEBHOOK="your_webhook_url"
python src/main.py morning
```
