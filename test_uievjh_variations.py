#!/usr/bin/env python3
"""
Test variations of Uievjh org code
"""

import requests
import json

def test_uievjh_variations():
    """Test variations of Uievjh org code"""
    print("🔍 Testing Uievjh Variations")
    print("="*50)
    
    # Original org code
    original_org = "Uievjh"
    email = "makey75125@hostbyt.com"
    
    # Different variations to try
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
        "Uievjh-org",
        "Uievjh-org1",
        "Uievjh-org123",
        "org-Uievjh",
        "org1-Uievjh",
        "org123-Uievjh",
        # Try with dots
        "Uievjh.org",
        "Uievjh.org1",
        "Uievjh.org123",
        "org.Uievjh",
        "org1.Uievjh",
        "org123.Uievjh",
        # Try with underscores
        "Uievjh_org",
        "Uievjh_org1",
        "Uievjh_org123",
        "org_Uievjh",
        "org1_Uievjh",
        "org123_Uievjh",
        # Try with spaces (URL encoded)
        "Uievjh%20org",
        "org%20Uievjh",
        # Try with common patterns
        "Uievjh_classplus",
        "Uievjh_cp",
        "Uievjh_edu",
        "Uievjh_school",
        "Uievjh_college",
        "Uievjh_university",
        "Uievjh_institute",
        "Uievjh_academy",
        "Uievjh_coaching",
        "Uievjh_tutorial",
        "Uievjh_training",
        "Uievjh_learning",
        "Uievjh_education",
        # Try with numbers
        "Uievjh1",
        "Uievjh2",
        "Uievjh3",
        "Uievjh01",
        "Uievjh02",
        "Uievjh03",
        "Uievjh001",
        "Uievjh002",
        "Uievjh003",
        # Try with year
        "Uievjh2024",
        "Uievjh2023",
        "Uievjh2022",
        "Uievjh2021",
        "Uievjh2020",
        # Try with month
        "Uievjh01",
        "Uievjh02",
        "Uievjh03",
        "Uievjh04",
        "Uievjh05",
        "Uievjh06",
        "Uievjh07",
        "Uievjh08",
        "Uievjh09",
        "Uievjh10",
        "Uievjh11",
        "Uievjh12",
        # Try with common words
        "Uievjh_demo",
        "Uievjh_test",
        "Uievjh_sample",
        "Uievjh_example",
        "Uievjh_trial",
        "Uievjh_free",
        "Uievjh_public",
        "Uievjh_private",
        "Uievjh_guest",
        "Uievjh_user",
        "Uievjh_admin",
        "Uievjh_student",
        "Uievjh_teacher",
        "Uievjh_staff",
        "Uievjh_faculty",
        "Uievjh_professor",
        "Uievjh_lecturer",
        "Uievjh_instructor",
        "Uievjh_trainer",
        "Uievjh_coach",
        "Uievjh_mentor",
        "Uievjh_tutor",
        "Uievjh_guide",
        "Uievjh_helper",
        "Uievjh_support",
        "Uievjh_help",
        "Uievjh_assist",
        "Uievjh_aid",
        "Uievjh_service",
        "Uievjh_provider",
        "Uievjh_platform",
        "Uievjh_system",
        "Uievjh_app",
        "Uievjh_application",
        "Uievjh_software",
        "Uievjh_tool",
        "Uievjh_utility",
        "Uievjh_resource",
        "Uievjh_material",
        "Uievjh_content",
        "Uievjh_data",
        "Uievjh_info",
        "Uievjh_information",
        "Uievjh_knowledge",
        "Uievjh_skill",
        "Uievjh_expertise",
        "Uievjh_experience",
        "Uievjh_practice",
        "Uievjh_exercise",
        "Uievjh_activity",
        "Uievjh_project",
        "Uievjh_task",
        "Uievjh_job",
        "Uievjh_work",
        "Uievjh_labor",
        "Uievjh_effort",
        "Uievjh_endeavor",
        "Uievjh_venture",
        "Uievjh_enterprise",
        "Uievjh_business",
        "Uievjh_company",
        "Uievjh_corporation",
        "Uievjh_organization",
        "Uievjh_institution",
        "Uievjh_establishment",
        "Uievjh_foundation",
        "Uievjh_association",
        "Uievjh_society",
        "Uievjh_community",
        "Uievjh_group",
        "Uievjh_team",
        "Uievjh_squad",
        "Uievjh_crew",
        "Uievjh_gang",
        "Uievjh_club",
        "Uievjh_union",
        "Uievjh_alliance",
        "Uievjh_partnership",
        "Uievjh_collaboration",
        "Uievjh_cooperation",
        "Uievjh_teamwork",
        "Uievjh_synergy",
        "Uievjh_harmony",
        "Uievjh_unity",
        "Uievjh_solidarity",
        "Uievjh_fellowship",
        "Uievjh_brotherhood",
        "Uievjh_sisterhood",
        "Uievjh_family",
        "Uievjh_household",
        "Uievjh_home",
        "Uievjh_residence",
        "Uievjh_dwelling",
        "Uievjh_abode",
        "Uievjh_habitat",
        "Uievjh_environment",
        "Uievjh_surroundings",
        "Uievjh_setting",
        "Uievjh_scene",
        "Uievjh_background",
        "Uievjh_context",
        "Uievjh_situation",
        "Uievjh_circumstance",
        "Uievjh_condition",
        "Uievjh_state",
        "Uievjh_status",
        "Uievjh_position",
        "Uievjh_location",
        "Uievjh_place",
        "Uievjh_site",
        "Uievjh_spot",
        "Uievjh_area",
        "Uievjh_zone",
        "Uievjh_region",
        "Uievjh_district",
        "Uievjh_sector",
        "Uievjh_field",
        "Uievjh_domain",
        "Uievjh_realm",
        "Uievjh_sphere",
        "Uievjh_world",
        "Uievjh_universe",
        "Uievjh_cosmos",
        "Uievjh_galaxy",
        "Uievjh_solar_system",
        "Uievjh_planet",
        "Uievjh_earth",
        "Uievjh_globe",
        "Uievjh_world",
        "Uievjh_planet_earth",
        "Uievjh_blue_planet",
        "Uievjh_third_rock",
        "Uievjh_terra",
        "Uievjh_gaia",
        "Uievjh_mother_earth",
        "Uievjh_nature",
        "Uievjh_environment",
        "Uievjh_ecosystem",
        "Uievjh_biosphere",
        "Uievjh_atmosphere",
        "Uievjh_climate",
        "Uievjh_weather",
        "Uievjh_temperature",
        "Uievjh_humidity",
        "Uievjh_pressure",
        "Uievjh_wind",
        "Uievjh_air",
        "Uievjh_oxygen",
        "Uievjh_nitrogen",
        "Uievjh_carbon",
        "Uievjh_hydrogen",
        "Uievjh_helium",
        "Uievjh_neon",
        "Uievjh_argon",
        "Uievjh_krypton",
        "Uievjh_xenon",
        "Uievjh_radon",
        "Uievjh_uranium",
        "Uievjh_plutonium",
        "Uievjh_thorium",
        "Uievjh_radium",
        "Uievjh_polonium",
        "Uievjh_astatine",
        "Uievjh_radon",
        "Uievjh_francium",
        "Uievjh_radium",
        "Uievjh_actinium",
        "Uievjh_thorium",
        "Uievjh_protactinium",
        "Uievjh_uranium",
        "Uievjh_neptunium",
        "Uievjh_plutonium",
        "Uievjh_americium",
        "Uievjh_curium",
        "Uievjh_berkelium",
        "Uievjh_californium",
        "Uievjh_einsteinium",
        "Uievjh_fermium",
        "Uievjh_mendelevium",
        "Uievjh_nobelium",
        "Uievjh_lawrencium",
        "Uievjh_rutherfordium",
        "Uievjh_dubnium",
        "Uievjh_seaborgium",
        "Uievjh_bohrium",
        "Uievjh_hassium",
        "Uievjh_meitnerium",
        "Uievjh_darmstadtium",
        "Uievjh_roentgenium",
        "Uievjh_copernicium",
        "Uievjh_nihonium",
        "Uievjh_flerovium",
        "Uievjh_moscovium",
        "Uievjh_livermorium",
        "Uievjh_tennessine",
        "Uievjh_oganesson"
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
    print("🚀 **UIEVJH VARIATIONS TESTER**")
    print("="*50)
    print("🔍 Testing variations of Uievjh org code...")
    
    # Test org variations
    valid_orgs = test_uievjh_variations()
    
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