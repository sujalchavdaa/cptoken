import requests
import time
import re
import json

def test_professional_token():
    print("🚀 Testing Professional Disposable Email for RPSC Token...")
    
    # Test org code
    org_code = "rpsc"
    
    # Step 1: Get org ID
    print("1️⃣ Getting org ID...")
    try:
        url = f"https://api.classplusapp.com/v2/orgs/{org_code}"
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
    try:
        # Try 1secmail API (most reliable)
        url = "https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1"
        response = requests.get(url)
        if response.status_code == 200:
            emails = response.json()
            if emails:
                email = emails[0]
                print(f"✅ Disposable email created: {email}")
            else:
                print("❌ Failed to create disposable email")
                return
        else:
            print("❌ Disposable email API failed")
            return
    except Exception as e:
        print(f"❌ Error creating disposable email: {e}")
        return
    
    # Step 3: Send OTP
    print("3️⃣ Sending OTP...")
    try:
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
            session_id = res.json()["data"]["sessionId"]
            print(f"✅ OTP sent successfully. Session ID: {session_id}")
        elif res.status_code == 403 and "limit exceeded" in res.text.lower():
            print("❌ Rate limit exceeded. Try after 6 hours.")
            return
        else:
            print(f"❌ Failed to send OTP: {res.text}")
            return
    except Exception as e:
        print(f"❌ Error sending OTP: {e}")
        return
    
    # Step 4: Check disposable email for OTP
    print("4️⃣ Checking disposable email for OTP...")
    start_time = time.time()
    max_wait = 60
    
    while time.time() - start_time < max_wait:
        try:
            # Check 1secmail API
            username, domain = email.split('@')
            url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}"
            response = requests.get(url)
            
            if response.status_code == 200:
                messages = response.json()
                print(f"📧 Checking emails... Found {len(messages)} emails")
                
                for message in messages:
                    msg_id = message.get('id')
                    if msg_id:
                        # Get message content
                        content_url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={domain}&id={msg_id}"
                        content_response = requests.get(content_url)
                        
                        if content_response.status_code == 200:
                            content_data = content_response.json()
                            body = content_data.get('body', '')
                            subject = content_data.get('subject', '')
                            
                            print(f"📨 Email subject: {subject}")
                            
                            if 'classplus' in subject.lower() or 'otp' in subject.lower():
                                print("🎯 Found Classplus email!")
                                otp_match = re.search(r'\b\d{6}\b', body)
                                if otp_match:
                                    otp = otp_match.group()
                                    print(f"✅ OTP found: {otp}")
                                    
                                    # Step 5: Verify OTP
                                    print("5️⃣ Verifying OTP...")
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
                                        
                                        # Step 6: Get access token
                                        print("6️⃣ Getting access token...")
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
                                            print(f"🎉 SUCCESS! Access Token: {token}")
                                            return True
                                        else:
                                            print("❌ Failed to get access token")
                                            return False
                                    else:
                                        print("❌ OTP verification failed")
                                        return False
                                else:
                                    print("❌ No OTP found in email content")
                            else:
                                print("📧 Not a Classplus email, skipping...")
            
            print("⏳ Waiting 5 seconds before next check...")
            time.sleep(5)
            
        except Exception as e:
            print(f"❌ Error checking disposable email: {e}")
            time.sleep(5)
    
    print("❌ No OTP found within timeout period")
    return False

if __name__ == "__main__":
    test_professional_token()