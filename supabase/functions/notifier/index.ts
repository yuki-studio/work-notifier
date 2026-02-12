import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { MESSAGES, CALENDAR_CONFIG } from "./config.ts";

const FEISHU_WEBHOOK_URL = Deno.env.get("FEISHU_WEBHOOK_URL") ?? "";

// Helper: Check if today is a workday
async function isWorkday(date: Date): Promise<boolean> {
  const dateStr = date.toISOString().split("T")[0]; // YYYY-MM-DD
  
  // 1. Check API
  try {
    const res = await fetch(`http://timor.tech/api/holiday/info/${dateStr}`, {
      headers: { "User-Agent": "Mozilla/5.0" },
    });
    if (res.ok) {
      const data = await res.json();
      if (data.code === 0) {
        // type: 0=workday, 1=weekend, 2=holiday, 3=makeup workday
        const type = data.type.type;
        return type === 0 || type === 3;
      }
    }
  } catch (e) {
    console.error("Timor API failed, using local config:", e);
  }

  // 2. Local Config Fallback
  if (CALENDAR_CONFIG.holidays.includes(dateStr)) return false;
  if (CALENDAR_CONFIG.makeup_workdays.includes(dateStr)) return true;

  // 3. Weekend Check (0=Sun, 6=Sat)
  // We use getUTCDay because the passed 'date' object is already shifted to Beijing Time (in UTC representation)
  const day = date.getUTCDay();
  return day !== 0 && day !== 6;
}

// Helper: Send to Feishu
async function sendFeishu(text: string) {
  if (!FEISHU_WEBHOOK_URL) {
    console.error("FEISHU_WEBHOOK_URL not set!");
    return;
  }
  
  const payload = {
    msg_type: "interactive",
    card: {
      header: {
        title: { tag: "plain_text", content: "🔔 提醒小助手" },
        template: "blue",
      },
      elements: [
        { tag: "div", text: { tag: "lark_md", content: text } },
        { tag: "hr" },
        {
          tag: "note",
          elements: [
            { tag: "plain_text", content: `发送时间: ${new Date().toLocaleString("zh-CN", { timeZone: "Asia/Shanghai" })}` }
          ]
        }
      ],
    },
  };

  const res = await fetch(FEISHU_WEBHOOK_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  
  console.log("Feishu response:", await res.text());
}

serve(async (req) => {
  // 1. Get Beijing Time
  // UTC time
  const now = new Date();
  // Create a date object that represents the time in Beijing (UTC+8)
  // We add 8 hours to the UTC timestamp
  const beijingTime = new Date(now.getTime() + 8 * 60 * 60 * 1000);
  
  const hour = beijingTime.getUTCHours(); // getUTCHours() of the shifted time is the hour in Beijing
  const dateStr = beijingTime.toISOString().split("T")[0];

  console.log(`Triggered at Beijing Time: ${beijingTime.toISOString()} (Hour: ${hour})`);

  // 2. Determine Slot
  let slot: "morning" | "lunch" | "evening" | null = null;
  
  // Allow a small window (e.g., if triggered at 09:30, hour is 9)
  if (hour === 9) slot = "morning";
  else if (hour === 12) slot = "lunch";
  else if (hour === 19) slot = "evening";
  else {
    return new Response(`No task for hour ${hour}. (Morning=9, Lunch=12, Evening=19)`, { status: 200 });
  }

  // 3. Check Workday
  const isWork = await isWorkday(beijingTime); 
  
  if (!isWork) {
    return new Response(`Today (${dateStr}) is not a workday. Skip.`, { status: 200 });
  }

  // 4. Send Message
  const messages = MESSAGES[slot];
  const text = messages[Math.floor(Math.random() * messages.length)];
  
  await sendFeishu(text);

  return new Response(`Sent ${slot} message: "${text}"`, { status: 200 });
});
