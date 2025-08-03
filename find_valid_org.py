#!/usr/bin/env python3
"""
Script to find valid organization codes
"""

import requests
import json

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

def find_valid_org_codes():
    """Find valid organization codes"""
    print("🔍 Searching for valid organization codes...")
    print("="*60)
    
    # Common org code patterns
    org_codes_to_try = [
        # Common patterns
        "demo", "test", "class", "school", "college", "university", "institute",
        "academy", "center", "coaching", "tutorial", "education", "learning",
        
        # Short codes
        "cp", "cl", "ed", "sc", "co", "un", "in", "ac", "ce", "tu", "le",
        
        # Number patterns
        "123", "456", "789", "001", "002", "003", "100", "200", "300",
        
        # Common words
        "rpsc", "upsc", "ssc", "bank", "railway", "police", "teacher",
        "student", "admin", "user", "guest", "public", "private",
        
        # Educational institutions
        "iit", "nit", "aiims", "neet", "jee", "cat", "mat", "gate",
        "upsc", "ssc", "bank", "railway", "teaching", "medical",
        
        # Random combinations
        "abc123", "test123", "demo123", "class123", "school123",
        "org1", "org2", "org3", "org123", "org456", "org789",
        "cp1", "cp2", "cp3", "cp123", "cp456", "cp789",
        
        # Real examples (if any)
        "classplus", "classplusapp", "classplusdemo", "classplustest",
        "rpsc", "upsc", "ssc", "bank", "railway", "police",
        
        # More variations
        "demo1", "demo2", "test1", "test2", "class1", "class2",
        "school1", "school2", "college1", "college2", "university1",
        "institute1", "institute2", "academy1", "academy2",
        
        # Short variations
        "d1", "d2", "t1", "t2", "c1", "c2", "s1", "s2", "u1", "u2",
        "i1", "i2", "a1", "a2", "ce1", "ce2", "tu1", "tu2", "le1", "le2"
    ]
    
    valid_orgs = []
    
    for org_code in org_codes_to_try:
        print(f"🔍 Trying: {org_code}")
        org_id = get_org_id(org_code)
        if org_id:
            print(f"   ✅ VALID: {org_code} -> {org_id}")
            valid_orgs.append((org_code, org_id))
        else:
            print(f"   ❌ Invalid: {org_code}")
    
    print("\n" + "="*60)
    print("📊 RESULTS:")
    print("="*60)
    
    if valid_orgs:
        print(f"✅ Found {len(valid_orgs)} valid organization(s):")
        for org_code, org_id in valid_orgs:
            print(f"   • {org_code} -> {org_id}")
    else:
        print("❌ No valid organizations found")
        print("💡 This might mean:")
        print("   • All tested codes are invalid")
        print("   • API is blocking requests")
        print("   • Need different approach")
    
    return valid_orgs

if __name__ == "__main__":
    find_valid_org_codes()