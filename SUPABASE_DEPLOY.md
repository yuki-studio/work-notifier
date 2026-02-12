# 🚀 部署到 Supabase 指南

既然我们决定升级到 **Supabase Edge Functions**，以下是保姆级操作步骤。请按顺序执行。

## 第一步：准备工作 (注册与安装)

1.  **注册账号**: 访问 [Supabase.com](https://supabase.com/) 并注册一个账号。
2.  **创建项目**: 登录后，点击 "New Project"，创建一个新项目（比如叫 `notifier-bot`）。
    *   记下你的 **Project Reference ID** (在 Settings -> General 中，形如 `abcdefghijklm`)。
    *   记下你的 **Project Password** (数据库密码，虽然我们暂时不用数据库，但最好记下来)。
3.  **安装 Supabase CLI** (Windows):

    打开你的 PowerShell 终端，运行以下命令安装包管理器 `Scoop` (如果你还没有的话)：
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser # 允许运行脚本
irm get.scoop.sh | iex
```

    然后安装 Supabase CLI：
```powershell
scoop bucket add supabase https://github.com/supabase/scoop-bucket.git
scoop install supabase
```

## 第二步：登录与关联

在终端中运行：

1.  **登录 Supabase**:
    ```powershell
    supabase login
    ```
    它会弹出一个浏览器窗口，点击确认即可。

2.  **关联你的项目**:
    将下面的 `YOUR_PROJECT_ID` 替换为你刚才记下的 ID：
    ```powershell
    supabase link --project-ref YOUR_PROJECT_ID
    ```
    (如果提示输入数据库密码，输入你创建项目时设置的密码)。

## 第三步：设置飞书密钥

你的代码需要知道飞书机器人的地址。我们通过“环境变量”来设置，不要把密钥写在代码里。

运行以下命令（将 `你的飞书Webhook地址` 换成真实的 URL）：
```powershell
supabase secrets set FEISHU_WEBHOOK_URL="你的飞书Webhook地址"
```

## 第四步：部署代码 🚀

见证奇迹的时刻。运行：
```powershell
supabase functions deploy notifier
```
如果没有报错，你会看到一个 URL，比如 `https://xyz...functions.supabase.co/notifier`。

## 第五步：设置定时任务 (Cron)


这是最后一步，让它自动运行。

1.  打开 [Supabase Dashboard](https://supabase.com/dashboard)。
2.  进入你的项目 -> **Integrations** (侧边栏) -> **Cron** (或者 Side Bar 里的 Edge Functions -> 点击 notifier -> 此时可能还没看到 Schedule 选项)。
3.  **推荐方法**：我们直接通过 SQL 开启定时任务。
    点击左侧侧边栏的 **SQL Editor**，新建一个 Query，粘贴以下代码并点击 **Run**：

```sql
-- 上班打卡 (北京时间 09:30)
select
  cron.schedule(
    'notifier-morning',
    '30 1 * * *', -- UTC时间 01:30
    $$
    select
      net.http_post(
          url:='https://YOUR_PROJECT_ID.supabase.co/functions/v1/notifier',
          headers:='{"Content-Type": "application/json", "Authorization": "Bearer YOUR_ANON_KEY"}'::jsonb
      ) as request_id;
    $$
  );

-- 午餐提醒 (北京时间 12:30)
select
  cron.schedule(
    'notifier-lunch',
    '30 4 * * *', -- UTC时间 04:30
    $$
    select
      net.http_post(
          url:='https://YOUR_PROJECT_ID.supabase.co/functions/v1/notifier',
          headers:='{"Content-Type": "application/json", "Authorization": "Bearer YOUR_ANON_KEY"}'::jsonb
      ) as request_id;
    $$
  );

-- 下班提醒 (北京时间 19:30)
select
  cron.schedule(
    'notifier-evening',
    '30 11 * * *', -- UTC时间 11:30
    $$
    select
      net.http_post(
          url:='https://YOUR_PROJECT_ID.supabase.co/functions/v1/notifier',
          headers:='{"Content-Type": "application/json", "Authorization": "Bearer YOUR_ANON_KEY"}'::jsonb
      ) as request_id;
    $$
  );
```
**注意**：请手动替换 SQL 中的 `YOUR_PROJECT_ID` 和 `YOUR_ANON_KEY` (可以在 Settings -> API 中找到 `anon public` key)。

---

### 🎉 大功告成！

现在，你的机器人已经运行在 Supabase 的全球边缘节点上了。
*   **它是免费的。**
*   **它是准时的。**
*   **它是用 TypeScript 写的。**

如果你想测试它，可以在终端运行：
```powershell
curl -X POST https://YOUR_PROJECT_ID.supabase.co/functions/v1/notifier
```
(它会根据当前时间判断发送什么消息)。
