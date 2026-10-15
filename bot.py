import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلًا إلياس 👋\n"
        "بوت مراقبة توفر حسابات إنستغرام.\n\n"
        "أرسل /check username لفحص حساب.\n"
        "مثال: /check instagram"
    )

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("استخدم الأمر هكذا:\n/check username")
        return

    username = context.args[0].lstrip("@")
    url = f"https://www.instagram.com/{username}/"

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15
        )

        if response.status_code == 200:
            await update.message.reply_text(
                f"الحساب @{username} يفتح حاليًا حسب الفحص العام.\n"
                "هذا لا يؤكد أنه كان محظورًا ثم استُعيد."
            )
        elif response.status_code == 404:
            await update.message.reply_text(
                f"الحساب @{username} غير موجود أو غير متاح.\n"
                "لا يمكن الجزم بأنه محظور."
            )
        else:
            await update.message.reply_text(
                f"تعذر التأكد من حالة @{username}.\n"
                f"رمز الاستجابة: {response.status_code}"
            )
    except requests.RequestException:
        await update.message.reply_text(
            "تعذر الفحص الآن؛ قد تكون هناك قيود على الوصول إلى إنستغرام."
        )

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN غير مضبوط في إعدادات الاستضافة")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))
    app.run_polling()

if __name__ == "__main__":
    main()
