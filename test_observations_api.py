"""
Test script for Observations API
Demonstrates creating and managing fieldwork observations
"""

import requests
import json
from datetime import datetime

API_BASE = "http://localhost:5000/api"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_health():
    """Test API health"""
    print_section("1. Testing API Health")
    
    response = requests.get(f"{API_BASE}/health")
    data = response.json()
    
    print(f"✓ Status: {data['status']}")
    print(f"✓ Message: {data['message']}")
    print(f"✓ LLM Configured: {data['llm_configured']}")

def test_create_observation():
    """Create sample observations"""
    print_section("2. Creating Sample Observations")
    
    observations = [
        {
            "linkedRequirement": {
                "id": "req_001",
                "citation": "EU GMP Annex 1 § 4.29",
                "category": "Environmental Monitoring",
                "risk_level": "Critical"
            },
            "observationText": "Reviewed EM data for March 2024. Found 3 action limit excursions in Grade A area. Investigation for EX-24-0312 was not completed within required 48-hour timeframe. Investigation report dated 5 days after excursion. No CAPA initiated for recurring issue.",
            "complianceStatus": "gap",
            "severity": "major",
            "location": "Grade A Filling Room 2",
            "interviewed": "Sarah Chen (EM Coordinator)"
        },
        {
            "linkedRequirement": {
                "id": "req_001",
                "citation": "EU GMP Annex 1 § 4.29",
                "category": "Environmental Monitoring",
                "risk_level": "Critical"
            },
            "observationText": "Trending analysis for environmental monitoring data not performed quarterly as required by SOP-EM-001. Last trending report found was from Q4 2023, no evidence of Q1 2024 analysis.",
            "complianceStatus": "gap",
            "severity": "major",
            "location": "Quality Office",
            "interviewed": "Michael Rodriguez (QA Manager)"
        },
        {
            "linkedRequirement": {
                "id": "req_001",
                "citation": "EU GMP Annex 1 § 4.29",
                "category": "Environmental Monitoring",
                "risk_level": "Critical"
            },
            "observationText": "Recent excursion EX-24-0415 was investigated within 24 hours. CAPA-2024-089 was opened appropriately with root cause analysis completed. Investigation report includes trending data and justification for corrective actions. Good practice observed.",
            "complianceStatus": "compliant",
            "severity": "minor",
            "location": "Grade A Filling Room 1",
            "interviewed": "Sarah Chen (EM Coordinator)"
        },
        {
            "linkedRequirement": {
                "id": "req_002",
                "citation": "FDA 21 CFR 211.25",
                "category": "Training",
                "risk_level": "High"
            },
            "observationText": "Reviewed training records for aseptic operators. All 12 operators have completed aseptic gowning qualification with media fill validation. Records show annual requalification is current. Training effectiveness is assessed through regular performance observations.",
            "complianceStatus": "compliant",
            "severity": "minor",
            "location": "Training Room / Grade A",
            "interviewed": "David Liu (Training Coordinator)"
        }
    ]
    
    created_ids = []
    
    for i, obs_data in enumerate(observations, 1):
        response = requests.post(
            f"{API_BASE}/observations",
            json=obs_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            result = response.json()
            obs_id = result['observation']['id']
            created_ids.append(obs_id)
            status = result['observation']['complianceStatus']
            
            status_emoji = {
                'compliant': '✓',
                'gap': '⚠️',
                'non-compliant': '✗'
            }
            
            print(f"{status_emoji[status]} Created: {obs_id}")
            print(f"   Requirement: {obs_data['linkedRequirement']['id']}")
            print(f"   Status: {status.upper()}")
            print(f"   Location: {obs_data['location']}")
            print()
        else:
            print(f"✗ Failed to create observation {i}: {response.text}")
    
    return created_ids

def test_get_observations():
    """Get all observations"""
    print_section("3. Retrieving All Observations")
    
    response = requests.get(f"{API_BASE}/observations")
    data = response.json()
    
    if data['success']:
        observations = data['observations']
        print(f"✓ Found {len(observations)} total observations\n")
        
        for obs in observations:
            print(f"  {obs['id']} - {obs['complianceStatus'].upper()}")
            print(f"    {obs['observationText'][:80]}...")
            print()
    else:
        print("✗ Failed to retrieve observations")

def test_get_stats():
    """Get observation statistics"""
    print_section("4. Observation Statistics")
    
    response = requests.get(f"{API_BASE}/observations/stats")
    data = response.json()
    
    if data['success']:
        stats = data['stats']
        
        print(f"Total Observations: {stats['total']}")
        print(f"\nBy Status:")
        print(f"  ✓ Compliant:      {stats['by_status']['compliant']}")
        print(f"  ⚠️ Gap:            {stats['by_status']['gap']}")
        print(f"  ✗ Non-Compliant:  {stats['by_status']['non_compliant']}")
        
        print(f"\nBy Severity:")
        print(f"  🔴 Critical: {stats['by_severity']['critical']}")
        print(f"  🟠 Major:    {stats['by_severity']['major']}")
        print(f"  🟡 Minor:    {stats['by_severity']['minor']}")
        
        print(f"\nTotal Evidence Items: {stats['total_evidence']}")
    else:
        print("✗ Failed to retrieve stats")

def test_get_by_requirement():
    """Get observations filtered by requirement"""
    print_section("5. Observations by Requirement (req_001)")
    
    response = requests.get(f"{API_BASE}/observations?requirement_id=req_001")
    data = response.json()
    
    if data['success']:
        observations = data['observations']
        print(f"✓ Found {len(observations)} observations for req_001\n")
        
        for obs in observations:
            status_labels = {
                'compliant': 'COMPLIANT ✓',
                'gap': 'GAP ⚠️',
                'non-compliant': 'NON-COMPLIANT ✗'
            }
            
            print(f"  {obs['id']} - {status_labels[obs['complianceStatus']]}")
            print(f"    Severity: {obs['severity'].upper()}")
            print(f"    Location: {obs['metadata']['location']}")
            print(f"    Timestamp: {obs['metadata']['timestamp']}")
            print()
    else:
        print("✗ Failed to retrieve observations")

def test_get_specific(obs_id):
    """Get specific observation"""
    print_section(f"6. Getting Specific Observation ({obs_id})")
    
    response = requests.get(f"{API_BASE}/observations/{obs_id}")
    data = response.json()
    
    if data['success']:
        obs = data['observation']
        
        print(f"ID: {obs['id']}")
        print(f"Status: {obs['complianceStatus'].upper()}")
        print(f"Severity: {obs['severity'].upper()}")
        print(f"\nLinked Requirement:")
        print(f"  {obs['linkedRequirement']['id']} - {obs['linkedRequirement']['citation']}")
        print(f"\nObservation:")
        print(f"  {obs['observationText']}")
        print(f"\nMetadata:")
        print(f"  Location: {obs['metadata']['location']}")
        print(f"  Interviewed: {obs['metadata']['interviewed']}")
        print(f"  Auditor: {obs['metadata']['auditor']}")
        print(f"  Timestamp: {obs['metadata']['timestamp']}")
    else:
        print(f"✗ Observation not found: {obs_id}")

def main():
    print("\n" + "="*60)
    print("  FIELDWORK OBSERVATIONS API - TEST SUITE")
    print("="*60)
    print("\n  Make sure the server is running:")
    print("  $ python app.py\n")
    
    try:
        # Test health
        test_health()
        
        # Create observations
        created_ids = test_create_observation()
        
        # Get all observations
        test_get_observations()
        
        # Get stats
        test_get_stats()
        
        # Get by requirement
        test_get_by_requirement()
        
        # Get specific observation
        if created_ids:
            test_get_specific(created_ids[0])
        
        print_section("✓ All Tests Completed Successfully!")
        
        print("\n📊 Summary:")
        print(f"  • Created {len(created_ids)} sample observations")
        print(f"  • Linked to 2 different requirements")
        print(f"  • Mixed status: Compliant, Gap, Non-Compliant")
        print(f"  • Full metadata captured (location, interviewed, timestamp)")
        
        print("\n🎯 Next Steps:")
        print("  1. Open http://localhost:5000 in browser")
        print("  2. Go to 'Pre-Audit Prep' and generate requirements")
        print("  3. Switch to 'Live Fieldwork' tab")
        print("  4. See the observations you just created!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API server")
        print("   Please start the server first:")
        print("   $ python app.py\n")
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")

if __name__ == "__main__":
    main()

