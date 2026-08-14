import os
from pathlib import Path

from flask import Flask, jsonify, request
from openai import OpenAI

app = Flask(**name**)

BASE_DIR = Path(**file**).resolve().parent
INDEX_FILE = BASE_DIR / "index.html"

API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY) if API_KEY else None

SYSTEM_PROMPT = """
تو Deep Solve AI هستی؛ یک دستیار هوش مصنوعی برای تفکر عمیق، تحلیل، حل مسئله و آموزش.

قواعد اصلی:

1. قبل از پاسخ، مسئله را دقیق بررسی کن.
2. داده‌های قطعی را از فرضیات جدا کن.
3. اگر اطلاعاتی کم است، آن را واضح اعلام کن.
4. از ساختن اطلاعات جعلی خودداری کن.
5. مسائل پیچیده را به مراحل کوچک و قابل فهم تقسیم کن.
6. در مسائل ریاضی، محاسبات را دقیق و مرحله‌به‌مرحله انجام بده.
7. در مسائل برنامه‌نویسی، ابتدا مشکل را شناسایی و سپس راه‌حل ارائه کن.
8. در مسائل علمی، بین واقعیت علمی و فرضیه تفاوت بگذار.
9. اگر چند راه‌حل وجود دارد، آنها را مقایسه کن.
10. مزایا، معایب، محدودیت‌ها و ریسک‌های مهم را بیان کن.
11. اگر پاسخ قطعی ممکن نیست، میزان اطمینان و دلیل آن را توضیح بده.
12. پاسخ‌ها را تا حد ممکن عمیق اما منظم ارائه کن.
13. زبان اصلی پاسخ فارسی است؛ در صورت نیاز از اصطلاحات انگلیسی تخصصی نیز استفاده کن.

برای مسائل پیچیده، در صورت مناسب بودن از این ساختار استفاده کن:

* درک مسئله
* اطلاعات موجود
* اطلاعات ناقص
* فرضیات
* تحلیل
* راه‌حل
* بررسی راه‌حل
* محدودیت‌ها و ریسک‌ها
* نتیجه
* مرحله بعدی پیشنهادی
  """

@app.route("/", methods=["GET"])
def home():
if INDEX_FILE.exists():
return INDEX_FILE.read_text(encoding="utf-8")

```
return jsonify({
    "success": True,
    "service": "Deep Solve AI",
    "message": "Backend is running.",
    "api": "/api/chat",
    "health": "/health"
})
```

@app.route("/health", methods=["GET"])
def health():
return jsonify({
"status": "ok",
"service": "Deep Solve AI",
"ai_configured": client is not None,
"index_exists": INDEX_FILE.exists()
})

@app.route("/api/chat", methods=["POST"])
def chat():
if client is None:
return jsonify({
"success": False,
"error": "OPENAI_API_KEY تنظیم نشده است."
}), 500

```
data = request.get_json(silent=True)

if not isinstance(data, dict):
    return jsonify({
        "success": False,
        "error": "بدنه درخواست باید JSON باشد."
    }), 400

message = str(data.get("message", "")).strip()

if not message:
    return jsonify({
        "success": False,
        "error": "پیام خالی است."
    }), 400

if len(message) > 12000:
    return jsonify({
        "success": False,
        "error": "پیام بیش از حد طولانی است."
    }), 400

try:
    response = client.responses.create(
        model="gpt-5-mini",
        instructions=SYSTEM_PROMPT,
        input=message
    )

    answer = response.output_text

    return jsonify({
        "success": True,
        "answer": answer
    })

except Exception as error:
    print(f"AI ERROR: {error}")

    return jsonify({
        "success": False,
        "error": "خطا در ارتباط با سرویس هوش مصنوعی."
    }), 500
```

if **name** == "**main**":
port = int(os.environ.get("PORT", 10000))

```
app.run(
    host="0.0.0.0",
    port=port
)
