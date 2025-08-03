import os
import telebot
from telebot import types
import requests
from flask import Flask
import threading
import random
import string
import time
import re

app = Flask("render_web")
def safe_send(send_func, *args, **kwargs):
    try:
        return send_func(*args, **kwargs)
    except Exception as e:
        print(f"[safe_send error] {e}")
        return None

@app.route("/")
def home():
    return "✅ Bot is running on Render!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

BOT_TOKEN = "7981010429:AAEAxW6kghZ5-uetl0OdRLuqvMopaEkzolQ"
bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}

def generate_random_email():
    """Generate a random email for OTP generation"""
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    domain = random.choice(['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com'])
    return f"{username}@{domain}"

def get_org_id(org_code):
    try:
        url = f"https://api.classplusapp.com/v2/orgs/{org_code}"
        headers = {
            "accept": "application/json, text/plain, */*",
            "user-agent": "Mozilla/5.0"
        }
        res = requests.get(url, headers=headers)
        if res.status_code == 200 and res.json()["status"] == "success":
            return res.json()["data"]["orgId"]
    except:
        return None
    return None

def send_otp(email, org_code, org_id):
    url = "https://api.classplusapp.com/v2/otp/generate"
    payload = {
        "countryExt": "91", "email": email, "orgCode": org_code,
        "viaEmail": "1", "viaSms": "0", "retry": 0, "orgId": org_id,
        "otpCount": 0, "identifier": email, "source": "web"
    }
    headers = {
        "accept": "application/json", "content-type": "application/json",
        "origin": "https://web.classplusapp.com", "referer": "https://web.classplusapp.com/",
        "region": "IN", "user-agent": "Mozilla/5.0", "api-version": "52", "device-id": "1234567890"
    }
    res = requests.post(url, json=payload, headers=headers)
    if res.status_code == 200 and "sessionId" in res.text:
        return res.json()["data"]["sessionId"]
    return None

def verify_otp(session_id, otp_code, org_id, email):
    url = "https://api.classplusapp.com/v2/users/verify"
    payload = {
        "otp": otp_code, "countryExt": "91", "sessionId": session_id,
        "orgId": org_id, "fingerprintId": "dummy", "email": email
    }
    headers = {
        "accept": "application/json", "content-type": "application/json",
        "origin": "https://web.classplusapp.com", "referer": "https://web.classplusapp.com/",
        "region": "IN", "user-agent": "Mozilla/5.0", "api-version": "52"
    }
    res = requests.post(url, json=payload, headers=headers)
    return res.status_code == 201 and "success" in res.text

def get_access_token():
    url = "https://event-api.classplusapp.com/analytics-api/v1/session/token"
    payload = {"source": 50, "source_app": "classplus"}
    headers = {
        "accept": "*/*", "content-type": "application/json",
        "origin": "https://web.classplusapp.com", "referer": "https://web.classplusapp.com/",
        "user-agent": "Mozilla/5.0"
    }
    res = requests.post(url, json=payload, headers=headers)
    if res.status_code == 200:
        return res.json()["data"]["token"]
    return None

def try_common_otps():
    """Try common OTP patterns that might work"""
    common_otps = [
        "123456", "000000", "111111", "222222", "333333", "444444", 
        "555555", "666666", "777777", "888888", "999999", "123123",
        "000123", "123000", "111222", "222333", "333444", "444555"
    ]
    return common_otps

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "👋 Welcome to Classplus Token Generator Bot!\n\n🔧 **Available Methods:**\n\n1️⃣ **Auto Mode** (Experimental): `/auto` - Just send org code\n2️⃣ **Manual Mode** (Reliable): `/manual` - Send org code + email + OTP\n\n💡 **Recommendation**: Use `/manual` for best results!")

@bot.message_handler(commands=['auto'])
def ask_org_code_auto(message):
    bot.send_message(message.chat.id, "🤖 **Auto Mode** (Experimental)\n\n⚠️ This mode tries common OTPs but may not work.\n\n📝 Send the ORG CODE:")
    bot.register_next_step_handler(message, process_org_code_auto)

def process_org_code_auto(message):
    org_code = message.text.strip()
    
    # Send processing message
    processing_msg = bot.send_message(message.chat.id, "🔄 Processing... Please wait.")
    
    try:
        # Step 1: Get org ID
        org_id = get_org_id(org_code)
        if not org_id:
            bot.edit_message_text("❌ Invalid ORG code.", chat_id=message.chat.id, message_id=processing_msg.message_id)
            return

        # Step 2: Generate random email
        email = generate_random_email()
        bot.edit_message_text(f"📧 Generated email: {email}\n🔄 Sending OTP...", chat_id=message.chat.id, message_id=processing_msg.message_id)
        
        # Step 3: Send OTP
        session_id = send_otp(email, org_code, org_id)
        if not session_id:
            bot.edit_message_text("❌ OTP send failed. Try again.", chat_id=message.chat.id, message_id=processing_msg.message_id)
            return

        # Step 4: Try common OTPs
        bot.edit_message_text("🔐 Trying common OTPs...", chat_id=message.chat.id, message_id=processing_msg.message_id)
        
        common_otps = try_common_otps()
        for i, otp in enumerate(common_otps):
            bot.edit_message_text(f"🔐 Trying OTP {i+1}/{len(common_otps)}: {otp}", chat_id=message.chat.id, message_id=processing_msg.message_id)
            
            verified = verify_otp(session_id, otp, org_id, email)
            if verified:
                # Step 5: Get access token
                bot.edit_message_text("✅ OTP verified!\n🔄 Getting access token...", chat_id=message.chat.id, message_id=processing_msg.message_id)
                
                token = get_access_token()
                if token:
                    bot.edit_message_text(
                        f"🎉 **Success!**\n\n"
                        f"📧 Email used: `{email}`\n"
                        f"🔑 OTP used: `{otp}`\n\n"
                        f"✅ **Your Access Token:**\n\n"
                        f"<code>{token}</code>", 
                        chat_id=message.chat.id, 
                        message_id=processing_msg.message_id,
                        parse_mode="HTML"
                    )
                else:
                    bot.edit_message_text("❌ Failed to get access token.", chat_id=message.chat.id, message_id=processing_msg.message_id)
                return
            else:
                # Wait a bit before next attempt
                time.sleep(1)
                continue
        
        # If all attempts failed
        bot.edit_message_text(
            "❌ Auto mode failed. Common OTPs didn't work.\n\n"
            "💡 **Try Manual Mode**:\n"
            "1. Send `/manual`\n"
            "2. Send `ORGCODE*EMAIL`\n"
            "3. Check your email for OTP\n"
            "4. Send the OTP back", 
            chat_id=message.chat.id, 
            message_id=processing_msg.message_id
        )

    except Exception as e:
        bot.edit_message_text(f"❌ Error: {str(e)}", chat_id=message.chat.id, message_id=processing_msg.message_id)

# Manual method (reliable)
@bot.message_handler(commands=['manual'])
def ask_org_email_manual(message):
    bot.send_message(message.chat.id, "📝 **Manual Mode** (Reliable)\n\nSend in `ORGCODE*EMAIL` format:\n\nExample: `ABC123*user@gmail.com`")
    bot.register_next_step_handler(message, process_org_email_manual)

def process_org_email_manual(message):
    try:
        org_code, email = message.text.strip().split("*")
        org_id = get_org_id(org_code)
        if not org_id:
            return bot.send_message(message.chat.id, "❌ Invalid ORG code.")

        session_id = send_otp(email, org_code, org_id)
        if not session_id:
            return bot.send_message(message.chat.id, "❌ OTP send failed. Try again.")

        # Save user state
        user_data[message.chat.id] = {
            "session_id": session_id,
            "org_id": org_id,
            "email": email
        }
        bot.send_message(message.chat.id, f"📥 OTP sent to {email}\n\n🔑 Please check your email and send the OTP here:")
        bot.register_next_step_handler(message, process_otp_manual)

    except:
        bot.send_message(message.chat.id, "❌ Invalid format. Use: ORGCODE*EMAIL")

def process_otp_manual(message):
    otp = message.text.strip()
    data = user_data.get(message.chat.id)

    if not data:
        return bot.send_message(message.chat.id, "⚠️ Session expired. Please send /manual again.")

    verified = verify_otp(data["session_id"], otp, data["org_id"], data["email"])
    if not verified:
        return bot.send_message(message.chat.id, "❌ OTP verification failed.")

    token = get_access_token()
    if token:
        bot.send_message(message.chat.id, f"✅ Your Access Token:\n\n<code>{token}</code>", parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, "❌ Failed to get token.")

# Keep old /token command for backward compatibility
@bot.message_handler(commands=['token'])
def token_command(message):
    bot.send_message(message.chat.id, "📝 Send in `ORGCODE*EMAIL` format:")
    bot.register_next_step_handler(message, process_org_email_manual)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    print("🤖 Classplus Token Bot is running... Waiting for messages.")
    bot.infinity_polling()


