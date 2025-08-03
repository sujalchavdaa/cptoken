#!/usr/bin/env python3
"""
Real Org Code Test
"""

import requests
import json

def test_real_org():
    """Test with real org code"""
    print("🚀 **REAL ORG CODE TESTER**")
    print("="*50)
    
    # Get org code from user
    org_code = input("📝 Enter your real org code: ").strip()
    email = "makey75125@hostbyt.com"
    
    print(f"\n🔍 Testing with:")
    print(f"   • Org Code: {org_code}")
    print(f"   • Email: {email}")
    print()
    
    # Step 1: Get org ID
    print("🔍 Step 1: Getting Organization ID...")
    org_id = get_org_id(org_code)
    if not org_id:
        print("❌ Invalid org code or org not found")
        return
    
    print(f"✅ Org ID: {org_id}")
    
    # Step 2: Send OTP
    print("\n🔍 Step 2: Sending OTP...")
    session_id = send_otp(email, org_code, org_id)
    
    if session_id == "RATE_LIMIT_EXCEEDED":
        print("⚠️ Rate limit exceeded. Cannot test further.")
        print("💡 Try again after 6 hours.")
        return
    elif not session_id:
        print("❌ Failed to send OTP")
        return
    
    print(f"✅ Session ID: {session_id}")
    
    # Step 3: Wait for OTP
    print(f"\n📝 **NEXT STEP:**")
    print(f"Please check your email: {email}")
    print(f"Enter the OTP you received:")
    
    otp = input("📱 Enter OTP: ").strip()
    
    if otp:
        print(f"\n🔍 Step 3: Verifying OTP...")
        user_token = verify_otp_and_get_user_token(session_id, otp, org_id, email)
        
        if user_token:
            print(f"\n🎉 **SUCCESS! User Authentication Token:**")
            print(f"✅ Token: {user_token}")
            
            # Decode token
            decode_user_token(user_token)
        else:
            print(f"\n❌ **Failed to verify OTP**")
    else:
        print(f"\n❌ **No OTP provided**")

def get_org_id(org_code):
    """Get organization ID from org code"""
    url = "https://api.classplusapp.com/v2/orgs/getOrgId"
    payload = {"orgCode": org_code}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "origin": "https://web.classplusapp.com",
        "referer": "https://web.classplusapp.com/",
        "user-agent": "Mozilla/5.0"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "data" in data and "orgId" in data["data"]:
                return data["data"]["orgId"]
            else:
                print(f"   ❌ Invalid response structure")
                return None
        else:
            print(f"   ❌ Failed with status {response.status_code}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def send_otp(email, org_code, org_id):
    """Send OTP to email"""
    url = "https://api.classplusapp.com/v2/users/sendOtp"
    payload = {
        "email": email,
        "countryExt": "91",
        "orgId": org_id,
        "fingerprintId": "dummy",
        "orgCode": org_code
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "origin": "https://web.classplusapp.com",
        "referer": "https://web.classplusapp.com/",
        "region": "IN",
        "user-agent": "Mozilla/5.0",
        "api-version": "52"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            if "data" in data and "sessionId" in data["data"]:
                return data["data"]["sessionId"]
            else:
                print(f"   ❌ Invalid response structure")
                return None
        elif response.status_code == 403 and "limit exceeded" in response.text.lower():
            return "RATE_LIMIT_EXCEEDED"
        else:
            print(f"   ❌ Failed with status {response.status_code}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def verify_otp_and_get_user_token(session_id, otp_code, org_id, email):
    """Verify OTP and return user authentication token"""
    url = "https://api.classplusapp.com/v2/users/verify"
    payload = {
        "otp": otp_code,
        "countryExt": "91",
        "sessionId": session_id,
        "orgId": org_id,
        "fingerprintId": "dummy",
        "email": email
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "origin": "https://web.classplusapp.com",
        "referer": "https://web.classplusapp.com/",
        "region": "IN",
        "user-agent": "Mozilla/5.0",
        "api-version": "52"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            try:
                data = response.json()
                print(f"   ✅ Success!")
                
                if "data" in data and "token" in data["data"]:
                    return data["data"]["token"]
                else:
                    print(f"   ❌ Token not found in response")
                    return None
                    
            except json.JSONDecodeError:
                print(f"   ❌ Error parsing JSON")
                return None
        else:
            print(f"   ❌ Failed with status {response.status_code}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def decode_user_token(token):
    """Decode and analyze user authentication token"""
    try:
        import base64
        
        # Split the token
        parts = token.split('.')
        if len(parts) != 3:
            print("❌ Invalid JWT token format")
            return
        
        # Decode payload
        payload = parts[1]
        payload += '=' * (4 - len(payload) % 4)
        payload_decoded = base64.b64decode(payload).decode('utf-8')
        payload_json = json.loads(payload_decoded)
        
        print("\n🔍 **USER AUTHENTICATION TOKEN ANALYSIS:**")
        print("="*50)
        print(f"✅ Token Type: User Authentication Token")
        print(f"✅ User ID: {payload_json.get('id', 'N/A')}")
        print(f"✅ Org ID: {payload_json.get('orgID', 'N/A')}")
        print(f"✅ Email: {payload_json.get('email', 'N/A')}")
        print(f"✅ Name: {payload_json.get('name', 'N/A')}")
        print(f"✅ Mobile: {payload_json.get('mobile', 'N/A')}")
        print(f"✅ Type: {payload_json.get('type', 'N/A')}")
        print(f"✅ Is First Login: {payload_json.get('isFirstLogin', 'N/A')}")
        print(f"✅ Login Via: {payload_json.get('loginVia', 'N/A')}")
        print(f"✅ Country Code: {payload_json.get('countryCode', 'N/A')}")
        print(f"✅ Default Language: {payload_json.get('defaultLanguage', 'N/A')}")
        print(f"✅ Issued At: {payload_json.get('iat', 'N/A')}")
        print(f"✅ Expires At: {payload_json.get('exp', 'N/A')}")
        
        print(f"\n📊 Full Token Payload:")
        print(json.dumps(payload_json, indent=2))
        
    except Exception as e:
        print(f"❌ Error decoding token: {e}")

if __name__ == "__main__":
    test_real_org()