"""
Test AI Observation Analysis Endpoint
Tests the /api/observations/analyze endpoint with real scenarios
"""

import requests
import json
from datetime import datetime

# Test configuration
BASE_URL = "http://localhost:5000"
ANALYZE_ENDPOINT = f"{BASE_URL}/api/observations/analyze"

# Sample requirements (simulating what was generated)
SAMPLE_REQUIREMENTS = [
    {
        "id": "req_001",
        "requirement_text (verbatim)": "When alert or action levels for microbial contamination are exceeded during environmental monitoring (EM), investigations must be initiated immediately. **21 CFR 211.42(c)(10)(iv)**",
        "suggested_audit_focus": "1. Review recent EM data for excursions\n2. Check investigation reports for timeliness\n3. Verify CAPA effectiveness",
        "risk_level": "Critical",
        "category": "Environmental Monitoring"
    },
    {
        "id": "req_002",
        "requirement_text (verbatim)": "Aseptic processing areas must maintain Grade A air quality during operations, with particle counts not exceeding specified limits. **EU GMP Annex 1 Section 4.18**",
        "suggested_audit_focus": "1. Review particle count data\n2. Verify HVAC validation\n3. Check gowning compliance",
        "risk_level": "Critical",
        "category": "Aseptic Processing"
    },
    {
        "id": "req_003",
        "requirement_text (verbatim)": "All personnel entering aseptic areas must complete annual aseptic technique qualification, including media fills and gowning qualification. **EU GMP Annex 1 Section 9.16**",
        "suggested_audit_focus": "1. Review training records\n2. Check qualification dates\n3. Verify requalification frequency",
        "risk_level": "High",
        "category": "Personnel Training"
    },
    {
        "id": "req_004",
        "requirement_text (verbatim)": "Batch records must be reviewed and approved by the quality unit before releasing any batch to distribution. **21 CFR 211.192**",
        "suggested_audit_focus": "1. Review batch record approval process\n2. Check for delays in approval\n3. Verify QA signatures",
        "risk_level": "Critical",
        "category": "Batch Release"
    },
    {
        "id": "req_005",
        "requirement_text (verbatim)": "Change control procedures must evaluate the impact of changes on product quality, including risk assessment and approval before implementation. **ICH Q10 Section 3.3**",
        "suggested_audit_focus": "1. Review recent change controls\n2. Verify risk assessments completed\n3. Check implementation timelines",
        "risk_level": "High",
        "category": "Change Control"
    }
]

# Test scenarios
TEST_SCENARIOS = [
    {
        "name": "EM Investigation Delay - Should match req_001",
        "observation": "During review of environmental monitoring data, found investigation EX-24-0312 for Grade A particle count excursion was initiated 5 days after the excursion was detected. Root cause analysis completed 10 days later. No CAPA was initiated.",
        "expected_requirement": "req_001",
        "expected_status": "non_compliant"
    },
    {
        "name": "Grade A Particle Count Excursion - Should match req_002",
        "observation": "Particle count data in Filling Room 2 shows Grade A area exceeded 20 particles (0.5 microns) during the afternoon shift on 2024-09-28. HVAC system validation expired 2 months ago.",
        "expected_requirement": "req_002",
        "expected_status": "non_compliant"
    },
    {
        "name": "Expired Training - Should match req_003",
        "observation": "Review of personnel training records shows that operator Sarah Chen's aseptic technique qualification expired 3 months ago (last qualified 2023-06-15). She has been working in aseptic areas during this period.",
        "expected_requirement": "req_003",
        "expected_status": "non_compliant"
    },
    {
        "name": "Batch Release Delay - Should match req_004",
        "observation": "Batch B2024-09-450 was released to distribution 5 days after manufacturing. Quality review was completed same day, but QA manager signature was delayed by 4 days due to vacation.",
        "expected_requirement": "req_004",
        "expected_status": "gap"
    },
    {
        "name": "Missing Risk Assessment - Should match req_005",
        "observation": "Change control CC-2024-0876 for new cleaning agent in Grade A areas shows approval from production manager but no documented risk assessment or QA approval prior to implementation.",
        "expected_requirement": "req_005",
        "expected_status": "non_compliant"
    },
    {
        "name": "Multi-modal with Image - Text + Image",
        "observation": "Observed gowning procedure in Grade A area.",
        "imageDescription": "Photo shows operator entering Grade A cleanroom without performing hand sanitization. Operator is wearing gloves but did not sanitize before gloving.",
        "expected_requirement": "req_003",
        "expected_status": "gap"
    },
    {
        "name": "Multi-modal with Audio - Text + Audio",
        "observation": "Interview with QA supervisor about batch release process.",
        "audioTranscription": "The supervisor stated: 'Sometimes we release batches before all testing is complete if we're under time pressure. We just mark it as conditional release.'",
        "expected_requirement": "req_004",
        "expected_status": "non_compliant"
    }
]

def print_section(title, char="="):
    """Print formatted section header"""
    print(f"\n{char * 80}")
    print(f"  {title}")
    print(f"{char * 80}\n")

def print_result(label, value, indent=0):
    """Print formatted result"""
    prefix = "  " * indent
    print(f"{prefix}{label}: {value}")

def test_ai_analysis(scenario):
    """Test a single observation analysis scenario"""
    print_section(f"TEST: {scenario['name']}", "-")
    
    # Build request payload
    payload = {
        "observationText": scenario["observation"],
        "requirements": SAMPLE_REQUIREMENTS
    }
    
    # Add optional fields
    if "imageDescription" in scenario:
        payload["imageDescription"] = scenario["imageDescription"]
    if "audioTranscription" in scenario:
        payload["audioTranscription"] = scenario["audioTranscription"]
    
    print("📝 OBSERVATION:")
    print(f"   {scenario['observation']}")
    if "imageDescription" in scenario:
        print(f"\n📸 IMAGE: {scenario['imageDescription']}")
    if "audioTranscription" in scenario:
        print(f"\n🎤 AUDIO: {scenario['audioTranscription']}")
    
    print("\n⏳ Analyzing with AI...")
    
    try:
        # Call API
        response = requests.post(
            ANALYZE_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        # Check response
        if response.status_code != 200:
            print(f"❌ ERROR: Status {response.status_code}")
            print(response.text)
            return False
        
        result = response.json()
        
        if not result.get("success"):
            print(f"❌ ERROR: {result.get('error', 'Unknown error')}")
            return False
        
        # Print results
        analysis = result["analysis"]
        
        print_section("✅ AI ANALYSIS COMPLETE", "-")
        
        # Matched requirements
        if "matched_requirements" in analysis and analysis["matched_requirements"]:
            print("🎯 MATCHED REQUIREMENTS:")
            for match in analysis["matched_requirements"]:
                req_id = match["requirement_id"]
                confidence = match.get("confidence", 0) * 100
                reasoning = match.get("reasoning", "No reasoning provided")
                print_result(f"• {req_id}", f"({confidence:.0f}% confidence)", 1)
                print_result("Reasoning", reasoning, 2)
                print()
            
            # Check if expected requirement is matched
            matched_ids = [m["requirement_id"] for m in analysis["matched_requirements"]]
            expected = scenario.get("expected_requirement")
            if expected:
                if expected in matched_ids:
                    print(f"   ✓ Correctly matched to {expected}")
                else:
                    print(f"   ⚠ Expected {expected}, got {matched_ids[0] if matched_ids else 'none'}")
        
        # Key findings
        if "key_findings" in analysis and analysis["key_findings"]:
            print("\n🔍 KEY FINDINGS:")
            for finding in analysis["key_findings"]:
                print(f"   • {finding}")
        
        # Compliance status
        if "compliance_status" in analysis:
            status = analysis["compliance_status"]
            status_icons = {
                "compliant": "✅",
                "gap": "⚠️",
                "non_compliant": "❌"
            }
            icon = status_icons.get(status, "❓")
            print(f"\n🎯 COMPLIANCE STATUS: {icon} {status.upper().replace('_', ' ')}")
            
            # Check if matches expected
            expected_status = scenario.get("expected_status")
            if expected_status and status != expected_status:
                print(f"   ⚠ Expected: {expected_status}")
        
        # Severity
        if "severity" in analysis:
            print(f"   Severity: {analysis['severity'].upper()}")
        
        # Analysis
        if "analysis" in analysis and analysis["analysis"]:
            print(f"\n💬 ANALYSIS:")
            print(f"   {analysis['analysis']}")
        
        # Recommendations
        if "recommendations" in analysis and analysis["recommendations"]:
            print("\n💡 RECOMMENDATIONS:")
            for rec in analysis["recommendations"]:
                print(f"   • {rec}")
        
        print()
        return True
        
    except requests.exceptions.Timeout:
        print("❌ ERROR: Request timeout (>60s)")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to server. Is it running?")
        print(f"   Make sure server is running on {BASE_URL}")
        return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def main():
    """Run all test scenarios"""
    print_section("🧪 AI OBSERVATION ANALYSIS TEST SUITE")
    
    print(f"Testing endpoint: {ANALYZE_ENDPOINT}")
    print(f"Number of scenarios: {len(TEST_SCENARIOS)}")
    print(f"Number of requirements: {len(SAMPLE_REQUIREMENTS)}")
    
    # Check server health
    print("\n🔍 Checking server health...")
    try:
        health_response = requests.get(f"{BASE_URL}/health", timeout=5)
        if health_response.status_code == 200:
            print("   ✓ Server is running")
        else:
            print(f"   ⚠ Server returned status {health_response.status_code}")
    except:
        print("   ❌ Server is not running!")
        print(f"\n   👉 Please start server first:")
        print(f"      python app.py")
        return
    
    # Run tests
    results = []
    for i, scenario in enumerate(TEST_SCENARIOS, 1):
        print(f"\n\n{'=' * 80}")
        print(f"  SCENARIO {i}/{len(TEST_SCENARIOS)}")
        print(f"{'=' * 80}")
        
        success = test_ai_analysis(scenario)
        results.append({
            "name": scenario["name"],
            "success": success
        })
        
        # Pause between tests
        if i < len(TEST_SCENARIOS):
            print("\n⏸  Pausing 2 seconds before next test...")
            import time
            time.sleep(2)
    
    # Summary
    print_section("📊 TEST SUMMARY")
    
    passed = sum(1 for r in results if r["success"])
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {passed/total*100:.0f}%\n")
    
    for i, result in enumerate(results, 1):
        icon = "✅" if result["success"] else "❌"
        print(f"{i}. {icon} {result['name']}")
    
    print()
    
    if passed == total:
        print("🎉 All tests passed! The AI observation analysis is working perfectly!")
    else:
        print("⚠️  Some tests failed. Check the logs above for details.")

if __name__ == "__main__":
    main()
