import requests
import telebot
from flask import Flask
import threading

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


BOT_TOKEN = "8276540429:AAGzVL1n5BHNaoRfEoZvoRzYGTNjklkIWTk"
bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}

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
        else:
            print("❌ Invalid ORG Code.")
            return None
    except Exception as e:
        print("❌ Error while getting orgId:", e)
        return None

def send_otp(email, org_code, org_id):
    url = "https://api.classplusapp.com/v2/otp/generate"
    payload = {
        "countryExt": "91",
        "email": email,
        "orgCode": org_code,
        "viaEmail": "1",
        "viaSms": "0",
        "retry": 0,
        "orgId": org_id,
        "otpCount": 0,
        "identifier": email,
        "source": "web"
    }
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://web.classplusapp.com",
        "referer": "https://web.classplusapp.com/",
        "region": "IN",
        "user-agent": "Mozilla/5.0",
        "api-version": "52",
        "device-id": "1753438844495"
    }
    res = requests.post(url, json=payload, headers=headers)
    if res.status_code == 200 and "sessionId" in res.text:
        session_id = res.json()["data"]["sessionId"]
        print("✅ OTP sent to:", email)
        return session_id
    else:
        print("❌ OTP not sent.")
        print(res.text)
        return None

def verify_otp(session_id, otp_code, org_code, org_id, email):
    url = "https://api.classplusapp.com/v2/users/verify"
    payload = {
        "otp": otp_code,
        "countryExt": "91",
        "sessionId": session_id,
        "orgId": org_id,
        "fingerprintId": "8e89c27a243a87688827af7a04499e47",
        "email": email
    }
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://web.classplusapp.com",
        "referer": "https://web.classplusapp.com/",
        "region": "IN",
        "user-agent": "Mozilla/5.0",
        "api-version": "52"
    }
    res = requests.post(url, json=payload, headers=headers)
    print("\n🔄 Verify Response:")
    print(res.text)
    if res.status_code == 201 and "success" in res.text:
        print("✅ OTP Verified.")
        return True
    else:
        print("❌ OTP verification failed.")
        return False

def get_access_token():
    url = "https://event-api.classplusapp.com/analytics-api/v1/session/token"
    payload = {
        "source": 50,
        "source_app": "classplus"
    }
    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "origin": "https://web.classplusapp.com",
        "referer": "https://web.classplusapp.com/",
        "user-agent": "Mozilla/5.0"
    }
    res = requests.post(url, json=payload, headers=headers)
    if res.status_code == 200:
        token = res.json()["data"]["token"]
        print("\n🔐 Access Token:")
        print(token)
        return token
    else:
        print("❌ Token not received.")
        return None

@bot.message_handler(commands=['start'])
def start(message):
    try:
        bot.send_message(message.chat.id, "👋 Welcome to Classplus Token Generator Bot.\nUse /token to start.")
    except Exception as e:
        print("Telegram send error:", e)

@bot.message_handler(commands=['token'])
def ask_org_email(message):
    try:
        bot.send_message(message.chat.id, "📝 Send your ORGCODE*EMAIL (e.g., abcd1234*test@gmail.com):")
        bot.register_next_step_handler(message, process_org_email)
    except Exception as e:
        print("Telegram send error:", e)

def process_org_email(message):
    try:
        user_input = message.text.strip()
        org_code, email = user_input.split("*")
    except:
        return bot.send_message(message.chat.id, "❌ Format invalid. Use ORGCODE*EMAIL")

    org_id = get_org_id(org_code)
    if not org_id:
        return bot.send_message(message.chat.id, "❌ Invalid ORG Code.")

    session = send_otp(email, org_code, org_id)
    if not session:
        return bot.send_message(message.chat.id, "❌ OTP not sent. Try again later.")

    user_data[message.chat.id] = {
        "session": session,
        "org_code": org_code,
        "org_id": org_id,
        "email": email
    }
    try:
        bot.send_message(message.chat.id, "📥 OTP sent to email. Please enter the OTP:")
        bot.register_next_step_handler(message, process_otp)
    except Exception as e:
        print("Telegram send error:", e)

def process_otp(message):
    otp = message.text.strip()
    data = user_data.get(message.chat.id)

    if not data:
        return bot.send_message(message.chat.id, "❌ Session expired. Use /token again.")

    verified = verify_otp(data["session"], otp, data["org_code"], data["org_id"], data["email"])
    if not verified:
        return bot.send_message(message.chat.id, "❌ OTP verification failed.")

    token = get_access_token()
    if token:
        try:
            bot.send_message(message.chat.id, f"✅ Your Access Token:\n\n<code>{token}</code>", parse_mode="HTML")
        except Exception as e:
            print("Telegram send error:", e)
    else:
        bot.send_message(message.chat.id, "❌ Token not received. Please try again.")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    print("🤖 Bot is running... Waiting for messages.")
    bot.infinity_polling()
