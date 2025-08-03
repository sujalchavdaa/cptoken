import requests
import time
import re
import json
import random
import string

def generate_custom_disposable_email():
    """Generate custom disposable email with different domains"""
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    domains = [
        'mu.undeadbanksu.com', 'temp-mail.org', 'guerrillamail.com',
        '10minutemail.com', 'tempmail.org', 'mailinator.com',
        'yopmail.com', 'getnada.com', 'sharklasers.com',
        'jioso.com', 'tempmailaddress.com', 'tmpmail.org',
        'mailnesia.com', 'maildrop.cc', 'tempr.email',
        'dispostable.com', 'mailinator2.com', 'spam4.me'
    ]
    domain = random.choice(domains)
    return f"{username}@{domain}"

def try_disposable_email_apis():
    """Try multiple disposable email APIs"""
    apis = [
        {
            "name": "10minutemail",
            "url": "https://10minutemail.net/address.api.php",
            "method": "GET"
        },
        {
            "name": "1secmail",
            "url": "https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1",
            "method": "GET"
        },
        {
            "name": "temp-mail.org",
            "url": "https://web2.temp-mail.org/mailbox",
            "method": "POST",
            "headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        }
    ]
    
    for api in apis:
        print(f"\n🔍 Trying {api['name']} API...")
        try:
            if api['method'] == 'GET':
                response = requests.get(api['url'])
            else:
                headers = api.get('headers', {})
                response = requests.post(api['url'], headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {api['name']} API working!")
                
                if api['name'] == "10minutemail":
                    email = data.get('mail_get_mail', '')
                    if email:
                        print(f"📧 Email: {email}")
                        return email
                elif api['name'] == "1secmail":
                    if data and len(data) > 0:
                        email = data[0]
                        print(f"📧 Email: {email}")
                        return email
                elif api['name'] == "temp-mail.org":
                    email = data.get('mailbox', '')
                    if email:
                        print(f"📧 Email: {email}")
                        return email
            else:
                print(f"❌ {api['name']} API failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error with {api['name']}: {e}")
    
    # Fallback to custom email
    print("\n🔄 Using custom disposable email...")
    email = generate_custom_disposable_email()
    print(f"📧 Custom email: {email}")
    return email

def get_org_id(org_code):
    """Get org ID for given org code"""
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
    """Send OTP to email"""
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

def verify_otp(session_id, otp_code, org_id, email):
    """Verify OTP"""
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
    """Get access token"""
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

def comprehensive_token_test():
    """Comprehensive test to get token"""
    print("🚀 Starting Comprehensive Token Test for RPSC...")
    
    org_code = "rpsc"
    max_attempts = 10
    successful_emails = []
    
    for attempt in range(max_attempts):
        print(f"\n🔄 Attempt {attempt + 1}/{max_attempts}")
        
        # Step 1: Get org ID
        print("1️⃣ Getting org ID...")
        org_id = get_org_id(org_code)
        if not org_id:
            print("❌ Invalid org code")
            continue
        print(f"✅ Org ID: {org_id}")
        
        # Step 2: Generate disposable email
        print("2️⃣ Generating disposable email...")
        email = try_disposable_email_apis()
        
        if not email:
            print("❌ Failed to create disposable email")
            continue
        
        # Step 3: Send OTP
        print("3️⃣ Sending OTP...")
        session_id = send_otp(email, org_code, org_id)
        
        if session_id == "RATE_LIMIT_EXCEEDED":
            print("⚠️ Rate limit exceeded. Trying different approach...")
            continue
        elif not session_id:
            print("❌ Failed to send OTP")
            continue
        
        print(f"✅ OTP sent successfully!")
        print(f"📧 Email: {email}")
        print(f"🔑 Session ID: {session_id}")
        
        # Save successful email for manual use
        successful_emails.append({
            "email": email,
            "session_id": session_id,
            "org_id": org_id
        })
        
        # Step 4: Try common OTPs (as backup)
        print("4️⃣ Trying common OTPs...")
        common_otps = ["123456", "000000", "111111", "222222", "333333", "444444", "555555", "666666", "777777", "888888", "999999"]
        
        for i, otp in enumerate(common_otps):
            print(f"🔐 Trying OTP {i+1}/{len(common_otps)}: {otp}")
            
            verified = verify_otp(session_id, otp, org_id, email)
            if verified:
                print("✅ OTP verified successfully!")
                
                # Step 5: Get access token
                print("5️⃣ Getting access token...")
                token = get_access_token()
                
                if token:
                    print(f"🎉 SUCCESS! Access Token: {token}")
                    
                    # Print summary
                    print("\n" + "="*50)
                    print("🎉 TOKEN SUCCESSFULLY GENERATED!")
                    print("="*50)
                    print(f"📧 Email used: {email}")
                    print(f"🔑 OTP used: {otp}")
                    print(f"🎫 Access Token: {token}")
                    print("="*50)
                    
                    return {
                        "success": True,
                        "email": email,
                        "otp": otp,
                        "token": token,
                        "session_id": session_id
                    }
                else:
                    print("❌ Failed to get access token")
            else:
                continue
        
        print("❌ Common OTPs didn't work. Trying next email...")
        time.sleep(2)  # Wait before next attempt
    
    # If no success, show manual options
    print("\n" + "="*50)
    print("📧 MANUAL OPTIONS AVAILABLE:")
    print("="*50)
    
    for i, email_data in enumerate(successful_emails):
        print(f"\n{i+1}. Email: {email_data['email']}")
        print(f"   Session ID: {email_data['session_id']}")
        print(f"   Use in bot: rpsc*{email_data['email']}")
    
    print("\n💡 Instructions:")
    print("1. Send /manual to bot")
    print("2. Send: rpsc*[EMAIL]")
    print("3. Check email for OTP")
    print("4. Send OTP back to bot")
    print("5. Get access token")
    
    return {
        "success": False,
        "manual_emails": successful_emails
    }

if __name__ == "__main__":
    result = comprehensive_token_test()
    
    if result["success"]:
        print(f"\n🎉 FINAL RESULT:")
        print(f"📧 Email: {result['email']}")
        print(f"🔑 OTP: {result['otp']}")
        print(f"🎫 Token: {result['token']}")
    else:
        print(f"\n📧 Manual emails available: {len(result['manual_emails'])}")