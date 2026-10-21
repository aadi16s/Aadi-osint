#!/usr/bin/env python3

import requests
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

BOT_TOKEN = "8843876003:AAFDjvABvCEQJubwHb1m5bLjLt7qyMZblaY"
API_URL = "https://ethicaltabbo.in/api/lookup"
API_KEY = "Sahil"

def get_number_info(number):
    try:
        url = f"{API_URL}?key={API_KEY}&mobile={number}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('status'):
                return data
        return None
    except:
        return None

def clean_data(data):
    """Remove unwanted fields like 'tabbo', 'remaining', etc."""
    if not data:
        return data
    
    # Remove unwanted top-level fields
    unwanted_keys = ['credit', 'telegram', 'channel', 'api_info']
    for key in unwanted_keys:
        if key in data:
            del data[key]
    
    # Remove unwanted fields from each record
    if 'data' in data and data['data']:
        unwanted_record_keys = ['id', 'alt_number']
        for record in data['data']:
            for key in unwanted_record_keys:
                if key in record:
                    del record[key]
    
    return data

async def start(update, context):
    await update.message.reply_text(
        "💀 DATA LEAKER OSINT BOT\n\n"
        "Send 10-digit number to get clean JSON data.\n"
        "📺 https://youtube.com/@geniushacker29\n"
        "🔥 ADIBHAI"
    )

async def handle_number(update, context):
    number = update.message.text.strip()
    
    if not number.isdigit() or len(number) != 10:
        await update.message.reply_text("❌ Send exactly 10 digits!")
        return
    
    msg = await update.message.reply_text("⏳ Searching...")
    data = get_number_info(number)
    
    if data:
        # Clean the data
        clean_data(data)
        
        result = json.dumps(data, indent=2, ensure_ascii=False)
        if len(result) > 4000:
            result = result[:4000] + "\n... (truncated)"
        await msg.edit_text(f"```json\n{result}\n```", parse_mode='Markdown')
    else:
        await msg.edit_text("❌ No data found!")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_number))
    print("💀 DATA LEAKER OSINT BOT is running!")
    app.run_polling()

if __name__ == "__main__":
    main()