"""
Test script for LLM endpoint
Tests the requirement generation without the frontend
"""
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test data - sample audit scope
test_audit_scope = {
    "facility": "PharmaCore Site C - Aseptic Filling Suite 2",
    "process_areas": [
        "Grade A/B Aseptic Filling Operations",
        "Environmental Monitoring Program",
        "Gowning & Personnel Flow",
        "Material Flow & Transfer"
    ],
    "products": "Injectable biologics (monoclonal antibodies - mAbs)",
    "time_period": "January 2024 - December 2024",
    "key_systems": [
        "QMS (MasterControl)",
        "Training System (Reliance)",
        "CAPA System",
        "Environmental Monitoring (Vaisala)"
    ],
    "regulatory_requirements": [
        "FDA 21 CFR Part 211 (cGMP)",
        "EU GMP Annex 1 (2022 - Sterile Manufacturing)",
        "ISO 14644 (Cleanroom Classification)",
        "PDA TR 13 (Environmental Monitoring)"
    ]
}

def test_health():
    """Test API health check"""
    print("\n" + "="*60)
    print("Testing API Health Check...")
    print("="*60)
    
    try:
        response = requests.get("http://localhost:5000/api/health", timeout=5)
        response.raise_for_status()
        data = response.json()
        print("✓ API is healthy")
        print(f"  Status: {data.get('status')}")
        print(f"  Model: {data.get('model')}")
        print(f"  Version: {data.get('version')}")
        return True
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to API server")
        print("  Make sure the server is running: python api_server.py")
        return False
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False

def test_databricks_config():
    """Test Databricks configuration"""
    print("\n" + "="*60)
    print("Checking Databricks Configuration...")
    print("="*60)
    
    host = os.getenv("DATABRICKS_HOST")
    token = os.getenv("DATABRICKS_TOKEN")
    
    if not host:
        print("✗ DATABRICKS_HOST not set in environment")
        return False
    if not token:
        print("✗ DATABRICKS_TOKEN not set in environment")
        return False
    
    print(f"✓ DATABRICKS_HOST: {host}")
    print(f"✓ DATABRICKS_TOKEN: {token[:10]}...{token[-10:] if len(token) > 20 else ''}")
    return True

def test_requirement_generation():
    """Test requirement generation endpoint"""
    print("\n" + "="*60)
    print("Testing Requirement Generation...")
    print("="*60)
    print("\nAudit Scope:")
    print(f"  Facility: {test_audit_scope['facility']}")
    print(f"  Process Areas: {len(test_audit_scope['process_areas'])} areas")
    print(f"  Products: {test_audit_scope['products']}")
    print(f"  Regulations: {len(test_audit_scope['regulatory_requirements'])} frameworks")
    
    try:
        print("\nCalling LLM endpoint (this may take 15-30 seconds)...")
        response = requests.post(
            "http://localhost:5000/api/generate-requirements",
            json=test_audit_scope,
            timeout=60
        )
        response.raise_for_status()
        
        data = response.json()
        
        print("\n" + "✓"*30)
        print("SUCCESS! Requirements Generated")
        print("✓"*30)
        print(f"\nTotal Requirements: {data.get('total_requirements', 0)}")
        print(f"Categories: {len(data.get('categories', []))}")
        
        # Display categories
        if data.get('categories'):
            print("\nCategories:")
            for cat in data['categories']:
                print(f"  • {cat['category_name']}: {cat['requirement_count']} requirements")
        
        # Display first requirement as sample
        if data.get('categories') and data['categories'][0].get('requirements'):
            print("\nSample Requirement:")
            req = data['categories'][0]['requirements'][0]
            print(f"  ID: {req['id']}")
            print(f"  Citation: {req['citation']}")
            print(f"  Risk Level: {req['risk_level']}")
            print(f"  Requirement: {req['requirement_text'][:100]}...")
        
        # Save full response
        output_file = "test_requirements_output.json"
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\nFull response saved to: {output_file}")
        
        return True
        
    except requests.exceptions.Timeout:
        print("✗ Request timed out (LLM took too long to respond)")
        print("  Try increasing the timeout or check your Databricks endpoint")
        return False
    except requests.exceptions.HTTPError as e:
        print(f"✗ HTTP Error: {e}")
        if e.response:
            print(f"  Response: {e.response.text}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("LLM ENDPOINT TEST SUITE")
    print("="*60)
    
    # Check configuration
    if not test_databricks_config():
        print("\n⚠ Configuration issues found. Please fix before continuing.")
        return
    
    # Test health
    if not test_health():
        print("\n⚠ API server not reachable. Please start the server first.")
        return
    
    # Test requirement generation
    test_requirement_generation()
    
    print("\n" + "="*60)
    print("Test suite complete!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()

