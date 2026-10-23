#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import base64
import re
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_URL = "https://shadowmere.xyz/api/b64sub/"

def fetch_subscription():
    try:
        req = urllib.request.Request(
            API_URL,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=15) as res:
            encoded = res.read().decode("utf-8").strip()
        return base64.b64decode(encoded).decode("utf-8")
    except Exception as e:
        return f"❌ အမှားအယွင်း: {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """👋 ကြိုဆိုပါတယ်!

📝 အသုံးပြုနိုင်တဲ့ညွှန်ကြားချက်များ-
/get  - လင့်ခ်အားလုံးကိုရယူရန်
/list - နိုင်ငံအလိုက်စာရင်းကြည့်ရန်
/help - အကူအညီရယူရန်"""
    await update.message.reply_text(text)

async def get_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 ဒေတာရယူနေသည်...")
    data = fetch_subscription()
    if len(data) > 4000:
        parts = [data[i:i+4000] for i in range(0, len(data), 4000)]
        for p in parts:
            await update.message.reply_text(p)
    else:
        await update.message.reply_text(data)

async def list_countries(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("("🔄 စာရင်းပြုစုနေသည်...")
    data = fetch_subscription()
    lines = [l.strip() for l in data.splitlines() if l.startswith("ss://")]
    countries = {}
    for l in lines:
        m = re.search(r"#([A-Z]{2})\s*.+$", l)
        if m:
            c = m.group(1)
            countries[c] = countries.get(c, 0) + 1
    text = "🌍 နိုင်ငံစာရင်း\n"
    for c, cnt in countries.items():
        text += f"{c}: {cnt} ခု\n"
    await update.message.reply_text(text)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""📖 အသုံးပြုနည်း
/get  = လင့်ခ်အားလုံး
/list = နိုင်ငံအလိုက်အရေအတွက်
/help = အကူအညီ

💡 ဒေတာအရင်းအမြစ်: shadowmere.xyz""")

def main():
    if not BOT_TOKEN:
        print("⚠️ BOT_TOKEN မရှိပါ")
        return
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('get', get_all))
    app.add_handler(CommandHandler('list', list_countries))
    app.add_handler(CommandHandler('help', help_cmd))
    print("✅ Bot အလုပ်လုပ်နေပါပြီ")
    app.run_polling()

if __name__ == "__main__":
    main()
