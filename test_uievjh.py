#!/usr/bin/env python3
"""
Test with Uievjh org code
"""

import requests
import json

def test_uievjh_org():
    """Test with Uievjh org code"""
    print("🚀 **UIEVJH ORG CODE TEST**")
    print("="*50)
    
    # Real data
    org_code = "Uievjh"
    email = "makey75125@hostbyt.com"
    
    print(f"📝 Testing with:")
    print(f"   • Org Code: {org_code}")
    print(f"   • Email: {email}")
    print()
    
    # Step 1: Get org ID
    print("🔍 Step 1: Getting Organization ID...")
    org_id = get_org_id(org_code)
    if not org_id:
        print("❌ Invalid org code or org not found")
        return None, None
    
    print(f"✅ Org ID: {org_id}")
    
    # Step 2: Send OTP
    print("\n🔍 Step 2: Sending OTP...")
    session_id = send_otp(email, org_code, org_id)
    
    if session_id == "RATE_LIMIT_EXCEEDED":
        print("⚠️ Rate limit exceeded. Cannot test further.")
        print("💡 Try again after 6 hours.")
        return None, None
    elif not session_id:
        print("❌ Failed to send OTP")
        return None, None
    
    print(f"✅ Session ID: {session_id}")
    
    return org_id, session_id

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
        print(f"   Response: {response.text[:200]}...")
        
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
        print(f"   Response: {response.text[:200]}...")
        
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
        print(f"   Response: {response.text[:200]}...")
        
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

def main():
    """Main function"""
    print("🔍 Testing Uievjh org code...")
    
    # Test with real data
    org_id, session_id = test_uievjh_org()
    
    if org_id and session_id:
        print(f"\n🎉 **SUCCESS! Ready for OTP verification!**")
        print(f"✅ Org ID: {org_id}")
        print(f"✅ Session ID: {session_id}")
        print(f"✅ Email: makey75125@hostbyt.com")
        print(f"\n📝 **Next Step:**")
        print(f"Please check your email and provide the OTP!")
        print(f"Then I'll verify the OTP and extract the user authentication token!")
        
        # Wait for user to provide OTP
        print(f"\n🔍 **WAITING FOR OTP:**")
        print("Please check your email and provide the OTP:")
        
        # For now, we'll simulate with a test OTP
        # In real scenario, user would provide the actual OTP
        print(f"\n💡 **Note:** In real scenario, you would provide the actual OTP from your email")
        print(f"   For testing, you can provide any OTP and I'll show you the process")
        
    else:
        print(f"\n❌ **Failed to get org ID or session ID**")
        print(f"💡 Please check the org code and try again")

if __name__ == "__main__":
    main()