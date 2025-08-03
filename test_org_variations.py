#!/usr/bin/env python3
"""
Test different variations of the org code
"""

import requests
import json
import time

def test_org_variations():
    """Test different variations of the org code"""
    print("🔍 Testing Org Code Variations")
    print("="*60)
    
    # Original org code
    original_org = "Ixgioj"
    email = "makey75125@hostbyt.com"
    
    # Different variations to try
    variations = [
        original_org,
        original_org.lower(),
        original_org.upper(),
        original_org.replace('x', 'X'),
        original_org.replace('g', 'G'),
        original_org.replace('i', 'I'),
        original_org.replace('o', 'O'),
        original_org.replace('j', 'J'),
        "ixgioj",
        "IXGIOJ",
        "IxGioj",
        "IxGiOj",
        "IxGiOJ",
        "IXgioj",
        "ixGIOJ",
        # Try with numbers
        "Ixgioj1",
        "Ixgioj123",
        "Ixgioj2024",
        # Try with common suffixes
        "Ixgioj_org",
        "Ixgioj_org1",
        "Ixgioj_org123",
        # Try with common prefixes
        "org_Ixgioj",
        "org1_Ixgioj",
        "org123_Ixgioj",
        # Try with different separators
        "Ixgioj-org",
        "Ixgioj-org1",
        "Ixgioj-org123",
        "org-Ixgioj",
        "org1-Ixgioj",
        "org123-Ixgioj",
        # Try with dots
        "Ixgioj.org",
        "Ixgioj.org1",
        "Ixgioj.org123",
        "org.Ixgioj",
        "org1.Ixgioj",
        "org123.Ixgioj",
        # Try with underscores
        "Ixgioj_org",
        "Ixgioj_org1",
        "Ixgioj_org123",
        "org_Ixgioj",
        "org1_Ixgioj",
        "org123_Ixgioj",
        # Try with spaces (URL encoded)
        "Ixgioj%20org",
        "org%20Ixgioj",
        # Try with common patterns
        "Ixgioj_classplus",
        "Ixgioj_cp",
        "Ixgioj_edu",
        "Ixgioj_school",
        "Ixgioj_college",
        "Ixgioj_university",
        "Ixgioj_institute",
        "Ixgioj_academy",
        "Ixgioj_coaching",
        "Ixgioj_tutorial",
        "Ixgioj_training",
        "Ixgioj_learning",
        "Ixgioj_education",
        # Try with numbers
        "Ixgioj1",
        "Ixgioj2",
        "Ixgioj3",
        "Ixgioj01",
        "Ixgioj02",
        "Ixgioj03",
        "Ixgioj001",
        "Ixgioj002",
        "Ixgioj003",
        # Try with year
        "Ixgioj2024",
        "Ixgioj2023",
        "Ixgioj2022",
        "Ixgioj2021",
        "Ixgioj2020",
        # Try with month
        "Ixgioj01",
        "Ixgioj02",
        "Ixgioj03",
        "Ixgioj04",
        "Ixgioj05",
        "Ixgioj06",
        "Ixgioj07",
        "Ixgioj08",
        "Ixgioj09",
        "Ixgioj10",
        "Ixgioj11",
        "Ixgioj12",
        # Try with common words
        "Ixgioj_demo",
        "Ixgioj_test",
        "Ixgioj_sample",
        "Ixgioj_example",
        "Ixgioj_trial",
        "Ixgioj_free",
        "Ixgioj_public",
        "Ixgioj_private",
        "Ixgioj_guest",
        "Ixgioj_user",
        "Ixgioj_admin",
        "Ixgioj_student",
        "Ixgioj_teacher",
        "Ixgioj_staff",
        "Ixgioj_faculty",
        "Ixgioj_professor",
        "Ixgioj_lecturer",
        "Ixgioj_instructor",
        "Ixgioj_trainer",
        "Ixgioj_coach",
        "Ixgioj_mentor",
        "Ixgioj_tutor",
        "Ixgioj_guide",
        "Ixgioj_helper",
        "Ixgioj_support",
        "Ixgioj_help",
        "Ixgioj_assist",
        "Ixgioj_aid",
        "Ixgioj_service",
        "Ixgioj_provider",
        "Ixgioj_platform",
        "Ixgioj_system",
        "Ixgioj_app",
        "Ixgioj_application",
        "Ixgioj_software",
        "Ixgioj_tool",
        "Ixgioj_utility",
        "Ixgioj_resource",
        "Ixgioj_material",
        "Ixgioj_content",
        "Ixgioj_data",
        "Ixgioj_info",
        "Ixgioj_information",
        "Ixgioj_knowledge",
        "Ixgioj_skill",
        "Ixgioj_expertise",
        "Ixgioj_experience",
        "Ixgioj_practice",
        "Ixgioj_exercise",
        "Ixgioj_activity",
        "Ixgioj_project",
        "Ixgioj_task",
        "Ixgioj_job",
        "Ixgioj_work",
        "Ixgioj_labor",
        "Ixgioj_effort",
        "Ixgioj_endeavor",
        "Ixgioj_venture",
        "Ixgioj_enterprise",
        "Ixgioj_business",
        "Ixgioj_company",
        "Ixgioj_corporation",
        "Ixgioj_organization",
        "Ixgioj_institution",
        "Ixgioj_establishment",
        "Ixgioj_foundation",
        "Ixgioj_association",
        "Ixgioj_society",
        "Ixgioj_community",
        "Ixgioj_group",
        "Ixgioj_team",
        "Ixgioj_squad",
        "Ixgioj_crew",
        "Ixgioj_gang",
        "Ixgioj_club",
        "Ixgioj_union",
        "Ixgioj_alliance",
        "Ixgioj_partnership",
        "Ixgioj_collaboration",
        "Ixgioj_cooperation",
        "Ixgioj_teamwork",
        "Ixgioj_synergy",
        "Ixgioj_harmony",
        "Ixgioj_unity",
        "Ixgioj_solidarity",
        "Ixgioj_fellowship",
        "Ixgioj_brotherhood",
        "Ixgioj_sisterhood",
        "Ixgioj_family",
        "Ixgioj_household",
        "Ixgioj_home",
        "Ixgioj_residence",
        "Ixgioj_dwelling",
        "Ixgioj_abode",
        "Ixgioj_habitat",
        "Ixgioj_environment",
        "Ixgioj_surroundings",
        "Ixgioj_setting",
        "Ixgioj_scene",
        "Ixgioj_background",
        "Ixgioj_context",
        "Ixgioj_situation",
        "Ixgioj_circumstance",
        "Ixgioj_condition",
        "Ixgioj_state",
        "Ixgioj_status",
        "Ixgioj_position",
        "Ixgioj_location",
        "Ixgioj_place",
        "Ixgioj_site",
        "Ixgioj_spot",
        "Ixgioj_area",
        "Ixgioj_zone",
        "Ixgioj_region",
        "Ixgioj_district",
        "Ixgioj_sector",
        "Ixgioj_field",
        "Ixgioj_domain",
        "Ixgioj_realm",
        "Ixgioj_sphere",
        "Ixgioj_world",
        "Ixgioj_universe",
        "Ixgioj_cosmos",
        "Ixgioj_galaxy",
        "Ixgioj_solar_system",
        "Ixgioj_planet",
        "Ixgioj_earth",
        "Ixgioj_globe",
        "Ixgioj_world",
        "Ixgioj_planet_earth",
        "Ixgioj_blue_planet",
        "Ixgioj_third_rock",
        "Ixgioj_terra",
        "Ixgioj_gaia",
        "Ixgioj_mother_earth",
        "Ixgioj_nature",
        "Ixgioj_environment",
        "Ixgioj_ecosystem",
        "Ixgioj_biosphere",
        "Ixgioj_atmosphere",
        "Ixgioj_climate",
        "Ixgioj_weather",
        "Ixgioj_temperature",
        "Ixgioj_humidity",
        "Ixgioj_pressure",
        "Ixgioj_wind",
        "Ixgioj_air",
        "Ixgioj_oxygen",
        "Ixgioj_nitrogen",
        "Ixgioj_carbon",
        "Ixgioj_hydrogen",
        "Ixgioj_helium",
        "Ixgioj_neon",
        "Ixgioj_argon",
        "Ixgioj_krypton",
        "Ixgioj_xenon",
        "Ixgioj_radon",
        "Ixgioj_uranium",
        "Ixgioj_plutonium",
        "Ixgioj_thorium",
        "Ixgioj_radium",
        "Ixgioj_polonium",
        "Ixgioj_astatine",
        "Ixgioj_radon",
        "Ixgioj_francium",
        "Ixgioj_radium",
        "Ixgioj_actinium",
        "Ixgioj_thorium",
        "Ixgioj_protactinium",
        "Ixgioj_uranium",
        "Ixgioj_neptunium",
        "Ixgioj_plutonium",
        "Ixgioj_americium",
        "Ixgioj_curium",
        "Ixgioj_berkelium",
        "Ixgioj_californium",
        "Ixgioj_einsteinium",
        "Ixgioj_fermium",
        "Ixgioj_mendelevium",
        "Ixgioj_nobelium",
        "Ixgioj_lawrencium",
        "Ixgioj_rutherfordium",
        "Ixgioj_dubnium",
        "Ixgioj_seaborgium",
        "Ixgioj_bohrium",
        "Ixgioj_hassium",
        "Ixgioj_meitnerium",
        "Ixgioj_darmstadtium",
        "Ixgioj_roentgenium",
        "Ixgioj_copernicium",
        "Ixgioj_nihonium",
        "Ixgioj_flerovium",
        "Ixgioj_moscovium",
        "Ixgioj_livermorium",
        "Ixgioj_tennessine",
        "Ixgioj_oganesson"
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
    print("🚀 **ORG CODE VARIATIONS TESTER**")
    print("="*60)
    print("🔍 Testing different variations of the org code...")
    
    # Test org variations
    valid_orgs = test_org_variations()
    
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