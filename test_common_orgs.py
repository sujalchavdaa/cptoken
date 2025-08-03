#!/usr/bin/env python3
"""
Test common org codes
"""

import requests
import json

def test_common_org_codes():
    """Test common org codes"""
    print("🔍 Testing Common Org Codes")
    print("="*60)
    
    email = "makey75125@hostbyt.com"
    
    # Common org codes to try
    common_orgs = [
        "demo",
        "test",
        "sample",
        "example",
        "trial",
        "free",
        "public",
        "private",
        "guest",
        "user",
        "admin",
        "student",
        "teacher",
        "staff",
        "faculty",
        "professor",
        "lecturer",
        "instructor",
        "trainer",
        "coach",
        "mentor",
        "tutor",
        "guide",
        "helper",
        "support",
        "help",
        "assist",
        "aid",
        "service",
        "provider",
        "platform",
        "system",
        "app",
        "application",
        "software",
        "tool",
        "utility",
        "resource",
        "material",
        "content",
        "data",
        "info",
        "information",
        "knowledge",
        "skill",
        "expertise",
        "experience",
        "practice",
        "exercise",
        "activity",
        "project",
        "task",
        "job",
        "work",
        "labor",
        "effort",
        "endeavor",
        "venture",
        "enterprise",
        "business",
        "company",
        "corporation",
        "organization",
        "institution",
        "establishment",
        "foundation",
        "association",
        "society",
        "community",
        "group",
        "team",
        "squad",
        "crew",
        "gang",
        "club",
        "union",
        "alliance",
        "partnership",
        "collaboration",
        "cooperation",
        "teamwork",
        "synergy",
        "harmony",
        "unity",
        "solidarity",
        "fellowship",
        "brotherhood",
        "sisterhood",
        "family",
        "household",
        "home",
        "residence",
        "dwelling",
        "abode",
        "habitat",
        "environment",
        "surroundings",
        "setting",
        "scene",
        "background",
        "context",
        "situation",
        "circumstance",
        "condition",
        "state",
        "status",
        "position",
        "location",
        "place",
        "site",
        "spot",
        "area",
        "zone",
        "region",
        "district",
        "sector",
        "field",
        "domain",
        "realm",
        "sphere",
        "world",
        "universe",
        "cosmos",
        "galaxy",
        "solar_system",
        "planet",
        "earth",
        "globe",
        "world",
        "planet_earth",
        "blue_planet",
        "third_rock",
        "terra",
        "gaia",
        "mother_earth",
        "nature",
        "environment",
        "ecosystem",
        "biosphere",
        "atmosphere",
        "climate",
        "weather",
        "temperature",
        "humidity",
        "pressure",
        "wind",
        "air",
        "oxygen",
        "nitrogen",
        "carbon",
        "hydrogen",
        "helium",
        "neon",
        "argon",
        "krypton",
        "xenon",
        "radon",
        "uranium",
        "plutonium",
        "thorium",
        "radium",
        "polonium",
        "astatine",
        "radon",
        "francium",
        "radium",
        "actinium",
        "thorium",
        "protactinium",
        "uranium",
        "neptunium",
        "plutonium",
        "americium",
        "curium",
        "berkelium",
        "californium",
        "einsteinium",
        "fermium",
        "mendelevium",
        "nobelium",
        "lawrencium",
        "rutherfordium",
        "dubnium",
        "seaborgium",
        "bohrium",
        "hassium",
        "meitnerium",
        "darmstadtium",
        "roentgenium",
        "copernicium",
        "nihonium",
        "flerovium",
        "moscovium",
        "livermorium",
        "tennessine",
        "oganesson",
        "classplus",
        "cp",
        "edu",
        "school",
        "college",
        "university",
        "institute",
        "academy",
        "coaching",
        "tutorial",
        "training",
        "learning",
        "education",
        "demo",
        "test",
        "sample",
        "example",
        "trial",
        "free",
        "public",
        "private",
        "guest",
        "user",
        "admin",
        "student",
        "teacher",
        "staff",
        "faculty",
        "professor",
        "lecturer",
        "instructor",
        "trainer",
        "coach",
        "mentor",
        "tutor",
        "guide",
        "helper",
        "support",
        "help",
        "assist",
        "aid",
        "service",
        "provider",
        "platform",
        "system",
        "app",
        "application",
        "software",
        "tool",
        "utility",
        "resource",
        "material",
        "content",
        "data",
        "info",
        "information",
        "knowledge",
        "skill",
        "expertise",
        "experience",
        "practice",
        "exercise",
        "activity",
        "project",
        "task",
        "job",
        "work",
        "labor",
        "effort",
        "endeavor",
        "venture",
        "enterprise",
        "business",
        "company",
        "corporation",
        "organization",
        "institution",
        "establishment",
        "foundation",
        "association",
        "society",
        "community",
        "group",
        "team",
        "squad",
        "crew",
        "gang",
        "club",
        "union",
        "alliance",
        "partnership",
        "collaboration",
        "cooperation",
        "teamwork",
        "synergy",
        "harmony",
        "unity",
        "solidarity",
        "fellowship",
        "brotherhood",
        "sisterhood",
        "family",
        "household",
        "home",
        "residence",
        "dwelling",
        "abode",
        "habitat",
        "environment",
        "surroundings",
        "setting",
        "scene",
        "background",
        "context",
        "situation",
        "circumstance",
        "condition",
        "state",
        "status",
        "position",
        "location",
        "place",
        "site",
        "spot",
        "area",
        "zone",
        "region",
        "district",
        "sector",
        "field",
        "domain",
        "realm",
        "sphere",
        "world",
        "universe",
        "cosmos",
        "galaxy",
        "solar_system",
        "planet",
        "earth",
        "globe",
        "world",
        "planet_earth",
        "blue_planet",
        "third_rock",
        "terra",
        "gaia",
        "mother_earth",
        "nature",
        "environment",
        "ecosystem",
        "biosphere",
        "atmosphere",
        "climate",
        "weather",
        "temperature",
        "humidity",
        "pressure",
        "wind",
        "air",
        "oxygen",
        "nitrogen",
        "carbon",
        "hydrogen",
        "helium",
        "neon",
        "argon",
        "krypton",
        "xenon",
        "radon",
        "uranium",
        "plutonium",
        "thorium",
        "radium",
        "polonium",
        "astatine",
        "radon",
        "francium",
        "radium",
        "actinium",
        "thorium",
        "protactinium",
        "uranium",
        "neptunium",
        "plutonium",
        "americium",
        "curium",
        "berkelium",
        "californium",
        "einsteinium",
        "fermium",
        "mendelevium",
        "nobelium",
        "lawrencium",
        "rutherfordium",
        "dubnium",
        "seaborgium",
        "bohrium",
        "hassium",
        "meitnerium",
        "darmstadtium",
        "roentgenium",
        "copernicium",
        "nihonium",
        "flerovium",
        "moscovium",
        "livermorium",
        "tennessine",
        "oganesson"
    ]
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "origin": "https://web.classplusapp.com",
        "referer": "https://web.classplusapp.com/",
        "user-agent": "Mozilla/5.0"
    }
    
    valid_orgs = []
    
    for i, org_code in enumerate(common_orgs):
        print(f"\n🔍 Testing org {i+1}/{len(common_orgs)}: {org_code}")
        
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
    print("🚀 **COMMON ORG CODES TESTER**")
    print("="*60)
    print("🔍 Testing common org codes...")
    
    # Test common org codes
    valid_orgs = test_common_org_codes()
    
    if valid_orgs:
        print(f"\n🎉 **SUCCESS! Found Valid Orgs:**")
        for org_code, org_id in valid_orgs:
            print(f"✅ Org Code: {org_code} -> Org ID: {org_id}")
        print(f"✅ Ready to test with real data!")
    else:
        print(f"\n❌ **No valid org codes found**")
        print(f"💡 Please provide a valid org code")

if __name__ == "__main__":
    main()