import requests
import json

def debug_otp_send():
    print("🔍 Debugging OTP Send for RPSC...")
    
    org_code = "rpsc"
    org_id = "2605"
    email = "test@example.com"
    
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
    
    print(f"📤 Sending request to: {url}")
    print(f"📋 Payload: {json.dumps(payload, indent=2)}")
    print(f"📋 Headers: {json.dumps(headers, indent=2)}")
    
    try:
        res = requests.post(url, json=payload, headers=headers)
        print(f"📥 Response Status: {res.status_code}")
        print(f"📥 Response Headers: {dict(res.headers)}")
        print(f"📥 Response Body: {res.text}")
        
        if res.status_code == 200:
            data = res.json()
            print(f"✅ Success! Data: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ Error: {res.status_code} - {res.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    debug_otp_send()