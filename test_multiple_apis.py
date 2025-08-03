import requests
import time
import re
import json

def test_multiple_disposable_apis():
    print("🔍 Testing Multiple Disposable Email APIs...")
    
    # Test different disposable email APIs
    apis = [
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
        },
        {
            "name": "10minutemail",
            "url": "https://10minutemail.net/address.api.php",
            "method": "GET"
        }
    ]
    
    for api in apis:
        print(f"\n🔍 Testing {api['name']} API...")
        try:
            if api['method'] == 'GET':
                response = requests.get(api['url'])
            else:
                headers = api.get('headers', {})
                response = requests.post(api['url'], headers=headers)
            
            print(f"📡 Response Status: {response.status_code}")
            print(f"📡 Response: {response.text[:200]}...")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {api['name']} API working!")
                
                # Try to extract email
                if api['name'] == "1secmail":
                    if data and len(data) > 0:
                        email = data[0]
                        print(f"📧 Email: {email}")
                        return email
                elif api['name'] == "temp-mail.org":
                    email = data.get('mailbox', '')
                    if email:
                        print(f"📧 Email: {email}")
                        return email
                elif api['name'] == "10minutemail":
                    email = data.get('mail_get_mail', '')
                    if email:
                        print(f"📧 Email: {email}")
                        return email
            else:
                print(f"❌ {api['name']} API failed")
                
        except Exception as e:
            print(f"❌ Error with {api['name']}: {e}")
    
    # Fallback - generate custom email
    print("\n🔄 Using fallback method...")
    import random
    import string
    
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    domains = [
        'mu.undeadbanksu.com', 'temp-mail.org', 'guerrillamail.com',
        '10minutemail.com', 'tempmail.org', 'mailinator.com',
        'yopmail.com', 'getnada.com', 'sharklasers.com'
    ]
    domain = random.choice(domains)
    email = f"{username}@{domain}"
    print(f"📧 Fallback email: {email}")
    return email

def test_rpsc_token():
    print("\n🚀 Testing RPSC Token Generation...")
    
    # Step 1: Get org ID
    print("1️⃣ Getting org ID...")
    try:
        url = f"https://api.classplusapp.com/v2/orgs/rpsc"
        headers = {
            "accept": "application/json, text/plain, */*",
            "user-agent": "Mozilla/5.0"
        }
        res = requests.get(url, headers=headers)
        if res.status_code == 200 and res.json()["status"] == "success":
            org_id = res.json()["data"]["orgId"]
            print(f"✅ Org ID found: {org_id}")
        else:
            print("❌ Invalid org code")
            return
    except Exception as e:
        print(f"❌ Error getting org ID: {e}")
        return
    
    # Step 2: Generate disposable email
    print("2️⃣ Generating disposable email...")
    email = test_multiple_disposable_apis()
    
    if not email:
        print("❌ Failed to create disposable email")
        return
    
    # Step 3: Send OTP
    print("3️⃣ Sending OTP...")
    try:
        url = "https://api.classplusapp.com/v2/otp/generate"
        payload = {
            "countryExt": "91", "email": email, "orgCode": "rpsc",
            "viaEmail": "1", "viaSms": "0", "retry": 0, "orgId": org_id,
            "otpCount": 0, "identifier": email, "source": "web"
        }
        headers = {
            "accept": "application/json", "content-type": "application/json",
            "origin": "https://web.classplusapp.com", "referer": "https://web.classplusapp.com/",
            "region": "IN", "user-agent": "Mozilla/5.0", "api-version": "52", "device-id": "1234567890"
        }
        res = requests.post(url, json=payload, headers=headers)
        
        print(f"📤 OTP Response Status: {res.status_code}")
        print(f"📤 OTP Response: {res.text}")
        
        if res.status_code == 200 and "sessionId" in res.text:
            session_id = res.json()["data"]["sessionId"]
            print(f"✅ OTP sent successfully. Session ID: {session_id}")
            
            # Show email details for manual check
            print(f"\n📧 **Email Details for Manual Check:**")
            print(f"📧 Email: {email}")
            print(f"🔑 Session ID: {session_id}")
            print(f"💡 Check the email manually for OTP")
            
        elif res.status_code == 403 and "limit exceeded" in res.text.lower():
            print("❌ Rate limit exceeded. Try after 6 hours.")
            return
        else:
            print(f"❌ Failed to send OTP")
            return
    except Exception as e:
        print(f"❌ Error sending OTP: {e}")
        return

if __name__ == "__main__":
    test_rpsc_token()