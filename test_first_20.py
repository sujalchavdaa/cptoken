#!/usr/bin/env python3
"""
Test first 20 variations of Uievjh
"""

import requests
import json

def test_first_20():
    """Test first 20 variations"""
    print("🔍 Testing First 20 Uievjh Variations")
    print("="*50)
    
    # Original org code
    original_org = "Uievjh"
    email = "makey75125@hostbyt.com"
    
    # First 20 variations to try
    variations = [
        original_org,
        original_org.lower(),
        original_org.upper(),
        "uievjh",
        "UIEVJH",
        "UieVjh",
        "UieVjH",
        "UieVJH",
        "UIevjh",
        "uiEVJH",
        # Try with numbers
        "Uievjh1",
        "Uievjh123",
        "Uievjh2024",
        # Try with common suffixes
        "Uievjh_org",
        "Uievjh_org1",
        "Uievjh_org123",
        # Try with common prefixes
        "org_Uievjh",
        "org1_Uievjh",
        "org123_Uievjh",
        # Try with different separators
        "Uievjh-org"
    ]
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "origin": "https://web.classplusapp.com",
        "referer": "https://web.classplusapp.com/",
        "user-agent": "Mozilla/5.0"
    }
    
    valid_orgs = []
    
    for i, org_code in enumerate(variations):
        print(f"\n🔍 Testing variation {i+1}/{len(variations)}: {org_code}")
        
        url = "https://api.classplusapp.com/v2/orgs/getOrgId"
        payload = {"orgCode": org_code}
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if "data" in data and "orgId" in data["data"]:
                    org_id = data["data"]["orgId"]
                    print(f"   ✅ VALID ORG FOUND: {org_code} -> {org_id}")
                    valid_orgs.append((org_code, org_id))
                    
                    # If we find a valid org, test OTP sending
                    print(f"   🔍 Testing OTP sending...")
                    test_otp_sending(org_code, org_id, email)
                    
                    # Only test first few valid orgs to avoid rate limiting
                    if len(valid_orgs) >= 3:
                        break
                else:
                    print(f"   ❌ Invalid response structure")
            else:
                print(f"   ❌ Status: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return valid_orgs

def test_otp_sending(org_code, org_id, email):
    """Test OTP sending for valid org"""
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
        print(f"   OTP Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            if "data" in data and "sessionId" in data["data"]:
                session_id = data["data"]["sessionId"]
                print(f"   ✅ OTP SENT SUCCESSFULLY!")
                print(f"   ✅ Session ID: {session_id}")
                print(f"   ✅ Ready for OTP verification!")
                return session_id
            else:
                print(f"   ❌ Invalid OTP response structure")
        elif response.status_code == 403 and "limit exceeded" in response.text.lower():
            print(f"   ⚠️ Rate limit exceeded")
        else:
            print(f"   ❌ OTP failed with status {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ OTP Error: {e}")
    
    return None

def main():
    """Main function"""
    print("🚀 **FIRST 20 UIEVJH VARIATIONS TESTER**")
    print("="*50)
    print("🔍 Testing first 20 variations of Uievjh org code...")
    
    # Test org variations
    valid_orgs = test_first_20()
    
    if valid_orgs:
        print(f"\n🎉 **SUCCESS! Found Valid Orgs:**")
        for org_code, org_id in valid_orgs:
            print(f"✅ Org Code: {org_code} -> Org ID: {org_id}")
        print(f"✅ Ready to test with real data!")
    else:
        print(f"\n❌ **No valid org codes found**")
        print(f"💡 Please check the org code spelling")

if __name__ == "__main__":
    main()