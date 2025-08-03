import requests
import json

def test_different_orgs():
    print("🧪 Testing Different Org Codes...")
    
    # Test different org codes
    test_orgs = ["rpsc", "abc123", "test123", "demo", "sample"]
    
    for org_code in test_orgs:
        print(f"\n🔍 Testing org code: {org_code}")
        
        # Step 1: Get org ID
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
                    print(f"✅ Org ID found: {org_id}")
                    
                    # Step 2: Try OTP send
                    email = "test@example.com"
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
                        print("✅ OTP sent successfully!")
                        return org_code, org_id
                    else:
                        print(f"❌ OTP failed: {otp_res.text}")
                else:
                    print(f"❌ Invalid org: {data.get('message', 'Unknown error')}")
            else:
                print(f"❌ Org not found: {res.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n❌ No working org codes found")
    return None, None

if __name__ == "__main__":
    test_different_orgs()