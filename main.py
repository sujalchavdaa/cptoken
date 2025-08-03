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
import json

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

def generate_disposable_email():
    """Generate disposable email using professional APIs"""
    try:
        # Try 1secmail API (most reliable)
        url = "https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1"
        response = requests.get(url)
        if response.status_code == 200:
            emails = response.json()
            if emails:
                return emails[0]
    except:
        pass
    
    try:
        # Try temp-mail.org API
        url = "https://web2.temp-mail.org/mailbox"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('mailbox', '')
    except:
        pass
    
    try:
        # Try 10minutemail API
        url = "https://10minutemail.net/address.api.php"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get('mail_get_mail', '')
    except:
        pass
    
    # Fallback - generate custom disposable email
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    domains = [
        'mu.undeadbanksu.com', 'temp-mail.org', 'guerrillamail.com',
        '10minutemail.com', 'tempmail.org', 'mailinator.com',
        'yopmail.com', 'getnada.com', 'sharklasers.com'
    ]
    domain = random.choice(domains)
    return f"{username}@{domain}"

def check_disposable_email_for_otp(email, max_wait=60):
    """Check disposable email for OTP using professional APIs"""
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        try:
            # Try 1secmail API
            if '@' in email:
                username, domain = email.split('@')
                url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}"
                response = requests.get(url)
                if response.status_code == 200:
                    messages = response.json()
                    for message in messages:
                        # Get message content
                        msg_id = message.get('id')
                        if msg_id:
                            content_url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={domain}&id={msg_id}"
                            content_response = requests.get(content_url)
                            if content_response.status_code == 200:
                                content_data = content_response.json()
                                body = content_data.get('body', '')
                                subject = content_data.get('subject', '')
                                
                                if 'classplus' in subject.lower() or 'otp' in subject.lower():
                                    # Extract OTP from email content
                                    otp_match = re.search(r'\b\d{6}\b', body)
                                    if otp_match:
                                        return otp_match.group()
            
            # Try temp-mail.org API
            url = "https://web2.temp-mail.org/messages"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                messages = data.get('messages', [])
                
                for message in messages:
                    if 'classplus' in message.get('subject', '').lower() or 'otp' in message.get('subject', '').lower():
                        content = message.get('body', '')
                        otp_match = re.search(r'\b\d{6}\b', content)
                        if otp_match:
                            return otp_match.group()
            
            # Try 10minutemail API
            url = "https://10minutemail.net/address.api.php"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                emails = data.get('mail_list', [])
                
                for mail in emails:
                    if 'classplus' in mail.get('mail_subject', '').lower() or 'otp' in mail.get('mail_subject', '').lower():
                        content = mail.get('mail_body', '')
                        otp_match = re.search(r'\b\d{6}\b', content)
                        if otp_match:
                            return otp_match.group()
            
            time.sleep(3)  # Wait 3 seconds before checking again
            
        except Exception as e:
            print(f"Error checking disposable email: {e}")
            time.sleep(3)
    
    return None

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
    elif res.status_code == 403 and "limit exceeded" in res.text.lower():
        return "RATE_LIMIT_EXCEEDED"
    else:
        return None

def verify_otp_and_get_user_token(session_id, otp_code, org_id, email):
    """Verify OTP and return user authentication token"""
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
    
    if res.status_code == 201:
        try:
            response_data = res.json()
            if "data" in response_data and "token" in response_data["data"]:
                return response_data["data"]["token"]
            else:
                print(f"❌ Token not found in response: {response_data}")
                return None
        except Exception as e:
            print(f"❌ Error parsing response: {e}")
            return None
    else:
        print(f"❌ OTP verification failed: {res.status_code} - {res.text}")
        return None

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

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "👋 Welcome to Classplus Token Generator Bot!\n\n🔧 **Available Methods:**\n\n1️⃣ **Auto Disposable Email** (NEW): `/auto` - Just send org code\n2️⃣ **Manual Mode** (Reliable): `/manual` - Send org code + email + OTP\n\n💡 **Recommendation**: Use `/auto` for best results!")

@bot.message_handler(commands=['auto'])
def ask_org_code_auto(message):
    bot.send_message(message.chat.id, "🤖 **Auto Disposable Email Mode** (NEW)\n\n📧 I'll create a disposable email and automatically get the OTP!\n\n📝 Send the ORG CODE:")
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

        # Step 2: Generate disposable email
        bot.edit_message_text("📧 Creating disposable email...", chat_id=message.chat.id, message_id=processing_msg.message_id)
        email = generate_disposable_email()
        
        if not email:
            bot.edit_message_text("❌ Failed to create disposable email. Try manual mode.", chat_id=message.chat.id, message_id=processing_msg.message_id)
            return
            
        bot.edit_message_text(f"📧 Disposable email created: {email}\n🔄 Sending OTP...", chat_id=message.chat.id, message_id=processing_msg.message_id)
        
        # Step 3: Send OTP
        session_id = send_otp(email, org_code, org_id)
        
        if session_id == "RATE_LIMIT_EXCEEDED":
            bot.edit_message_text(
                "⚠️ **Rate Limit Exceeded!**\n\n"
                "🚫 Classplus ne 6 hours ka limit lagaya hai.\n\n"
                "💡 **Solutions:**\n"
                "1️⃣ **Wait 6 hours** and try again\n"
                "2️⃣ **Use Manual Mode**: `/manual`\n"
                "3️⃣ **Try different org code**\n\n"
                "📝 Manual mode mein aap apna real email use kar sakte hain.", 
                chat_id=message.chat.id, 
                message_id=processing_msg.message_id
            )
            return
        elif not session_id:
            bot.edit_message_text("❌ OTP send failed. Try again.", chat_id=message.chat.id, message_id=processing_msg.message_id)
            return

        # Step 4: Check disposable email for OTP
        bot.edit_message_text("📥 Checking disposable email for OTP...", chat_id=message.chat.id, message_id=processing_msg.message_id)
        
        otp = check_disposable_email_for_otp(email, max_wait=60)
        
        if otp:
            bot.edit_message_text(f"✅ OTP found: {otp}\n🔄 Verifying OTP and getting user token...", chat_id=message.chat.id, message_id=processing_msg.message_id)
            
            # Step 5: Verify OTP and get user authentication token
            user_token = verify_otp_and_get_user_token(session_id, otp, org_id, email)
            if user_token:
                bot.edit_message_text(
                    f"🎉 **SUCCESS! User Authentication Token Found!**\n\n"
                    f"📧 Disposable email: `{email}`\n"
                    f"🔑 OTP used: `{otp}`\n\n"
                    f"✅ **Your User Authentication Token:**\n\n"
                        f"<code>{user_token}</code>", 
                        chat_id=message.chat.id, 
                        message_id=processing_msg.message_id,
                        parse_mode="HTML"
                    )
                else:
                    bot.edit_message_text("❌ Failed to get access token.", chat_id=message.chat.id, message_id=processing_msg.message_id)
                return
            else:
                bot.edit_message_text("❌ OTP verification failed.", chat_id=message.chat.id, message_id=processing_msg.message_id)
        else:
            bot.edit_message_text(
                f"📧 **Disposable Email Created Successfully!**\n\n"
                f"📧 Email: `{email}`\n"
                f"🔑 Session ID: `{session_id}`\n\n"
                f"💡 **Next Steps:**\n"
                f"1️⃣ Check disposable email: {email}\n"
                f"2️⃣ Find the OTP email from Classplus\n"
                f"3️⃣ Send the OTP here\n\n"
                f"🔧 **Or use Manual Mode**: `/manual`", 
                chat_id=message.chat.id, 
                message_id=processing_msg.message_id,
                parse_mode="HTML"
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
        
        if session_id == "RATE_LIMIT_EXCEEDED":
            return bot.send_message(message.chat.id, 
                "⚠️ **Rate Limit Exceeded!**\n\n"
                "🚫 Classplus ne 6 hours ka limit lagaya hai.\n\n"
                "💡 **Wait 6 hours** and try again.")
        elif not session_id:
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

    user_token = verify_otp_and_get_user_token(data["session_id"], otp, data["org_id"], data["email"])
    if user_token:
        bot.send_message(message.chat.id, f"🎉 **SUCCESS! User Authentication Token Found!**\n\n✅ **Your User Authentication Token:**\n\n<code>{user_token}</code>", parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, "❌ OTP verification failed or token not found.")

# Keep old /token command for backward compatibility
@bot.message_handler(commands=['token'])
def token_command(message):
    bot.send_message(message.chat.id, "📝 Send in `ORGCODE*EMAIL` format:")
    bot.register_next_step_handler(message, process_org_email_manual)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    print("🤖 Classplus Token Bot with Professional Disposable Email is running... Waiting for messages.")
    bot.infinity_polling()


