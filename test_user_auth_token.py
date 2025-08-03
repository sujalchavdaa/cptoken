#!/usr/bin/env python3
"""
Test Script for User Authentication Token Extraction
This script tests the proper user authentication token flow
"""

import requests
import json
import time

def get_org_id(org_code):
    """Get organization ID from org code"""
    url = "https://api.classplusapp.com/v2/orgs/getOrgId"
    payload = {"orgCode": org_code}
    headers = {
        "accept": "application/json", "content-type": "application/json",
        "origin": "https://web.classplusapp.com", "referer": "https://web.classplusapp.com/",
        "user-agent": "Mozilla/5.0"
    }
    res = requests.post(url, json=payload, headers=headers)
    if res.status_code == 200:
        return res.json()["data"]["orgId"]
    return None

def send_otp(email, org_code, org_id):
    """Send OTP to email"""
    url = "https://api.classplusapp.com/v2/users/sendOtp"
    payload = {
        "email": email, "countryExt": "91", "orgId": org_id,
        "fingerprintId": "dummy", "orgCode": org_code
    }
    headers = {
        "accept": "application/json", "content-type": "application/json",
        "origin": "https://web.classplusapp.com", "referer": "https://web.classplusapp.com/",
        "region": "IN", "user-agent": "Mozilla/5.0", "api-version": "52"
    }
    res = requests.post(url, json=payload, headers=headers)
    
    if res.status_code == 201:
        return res.json()["data"]["sessionId"]
    elif res.status_code == 403 and "limit exceeded" in res.text.lower():
        return "RATE_LIMIT_EXCEEDED"
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
    
    print(f"🔍 Verify OTP Response Status: {res.status_code}")
    print(f"🔍 Response Text: {res.text[:200]}...")
    
    if res.status_code == 201:
        try:
            response_data = res.json()
            print(f"🔍 Full Response Data: {json.dumps(response_data, indent=2)}")
            
            if "data" in response_data and "token" in response_data["data"]:
                return response_data["data"]["token"]
            else:
                print(f"❌ Token not found in response structure")
                return None
        except Exception as e:
            print(f"❌ Error parsing response: {e}")
            return None
    else:
        print(f"❌ OTP verification failed: {res.status_code} - {res.text}")
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
        print("="*60)
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

def test_user_auth_token_flow():
    """Test the complete user authentication token flow"""
    print("🚀 Testing User Authentication Token Flow")
    print("="*60)
    
    # Test different org codes
    org_codes_to_try = ["rpsc", "abc123", "test123", "demo", "classplus", "cp", "org1", "org2"]
    
    valid_org_code = None
    valid_org_id = None
    
    print("🔍 Testing different org codes...")
    for org_code in org_codes_to_try:
        print(f"   • Trying: {org_code}")
        org_id = get_org_id(org_code)
        if org_id:
            print(f"   ✅ Found valid org: {org_code} -> {org_id}")
            valid_org_code = org_code
            valid_org_id = org_id
            break
        else:
            print(f"   ❌ Invalid: {org_code}")
    
    if not valid_org_code:
        print("❌ No valid org codes found. Using 'rpsc' as fallback.")
        valid_org_code = "rpsc"
        valid_org_id = get_org_id(valid_org_code)
        if not valid_org_id:
            print("❌ Cannot proceed without valid org code")
            return
    
    # Test parameters
    test_email = "test@example.com"  # You can change this
    
    print(f"\n📝 Testing with:")
    print(f"   • Org Code: {valid_org_code}")
    print(f"   • Org ID: {valid_org_id}")
    print(f"   • Email: {test_email}")
    print()
    
    # Step 2: Send OTP
    print("🔍 Step 2: Sending OTP...")
    session_id = send_otp(test_email, valid_org_code, valid_org_id)
    
    if session_id == "RATE_LIMIT_EXCEEDED":
        print("⚠️ Rate limit exceeded. Cannot test further.")
        print("💡 Try again after 6 hours or use a different org code.")
        return
    elif not session_id:
        print("❌ Failed to send OTP")
        return
    
    print(f"✅ Session ID: {session_id}")
    
    # Step 3: Manual OTP input
    print("\n🔍 Step 3: Manual OTP Verification")
    print("📝 Please check your email and enter the OTP:")
    otp = input("Enter OTP: ").strip()
    
    if not otp:
        print("❌ No OTP provided")
        return
    
    # Step 4: Verify OTP and get user token
    print("\n🔍 Step 4: Verifying OTP and extracting user token...")
    user_token = verify_otp_and_get_user_token(session_id, otp, valid_org_id, test_email)
    
    if user_token:
        print(f"\n🎉 **SUCCESS! User Authentication Token Found!**")
        print(f"✅ Token: {user_token}")
        
        # Decode and analyze the token
        decode_user_token(user_token)
        
    else:
        print("❌ Failed to get user authentication token")
        print("💡 This might be due to:")
        print("   • Invalid OTP")
        print("   • Rate limiting")
        print("   • API changes")

if __name__ == "__main__":
    test_user_auth_token_flow()