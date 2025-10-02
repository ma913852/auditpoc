# Fieldwork Observations - User Experience Design

## 🎯 Concept Overview

During fieldwork, auditors need to **capture observations** while having **full context** of the requirements they're auditing against. This design creates a seamless connection between AI-generated requirements and real-time observations.

---

## 📱 User Experience Flow

### **Phase 1: Pre-Fieldwork Review**
```
Auditor reviews AI-generated requirements
    ↓
Selects requirements to focus on during fieldwork
    ↓
System generates observation templates linked to requirements
    ↓
Ready for fieldwork!
```

### **Phase 2: Live Fieldwork**
```
Auditor walks facility/reviews documents
    ↓
Taps "New Observation" button
    ↓
Selects linked requirement (or creates standalone)
    ↓
Records observation with rich evidence
    ↓
Auto-saves to cloud, syncs across team
```

### **Phase 3: Post-Fieldwork Review**
```
All observations grouped by requirement
    ↓
Review compliance status
    ↓
Promote observations to findings
    ↓
Export to final report
```

---

## 🎨 Screen-by-Screen Design

### **Screen 1: Requirements Checklist View**

```
┌────────────────────────────────────────────────────────────┐
│  🏭 Live Fieldwork - Environmental Monitoring              │
│  ────────────────────────────────────────────────────────  │
│                                                            │
│  📋 Requirements (10)  |  📝 Observations (23)  |  ⚠️ Gaps (5) │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ Search requirements or create observation...         │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  Filters: [All] [Critical] [High] [Medium] [Low]          │
│  Status:  [All] [✓ Compliant] [⚠ Gap] [✗ Non-Compliant]  │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ 🔴 req_001 - CRITICAL                    3 observations│ │
│  │ EU GMP Annex 1 § 4.29                                  │ │
│  │                                                        │ │
│  │ When alert levels or action limits are exceeded,      │ │
│  │ investigate the cause...                               │ │
│  │                                                        │ │
│  │ Status: ⚠️ GAP IDENTIFIED                               │ │
│  │                                                        │ │
│  │ [View Details] [+ Add Observation]                    │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ 🟠 req_002 - HIGH                         1 observation│ │
│  │ 21 CFR 211.25                                          │ │
│  │                                                        │ │
│  │ Personnel qualification before working in Grade A/B... │ │
│  │                                                        │ │
│  │ Status: ✓ COMPLIANT                                    │ │
│  │                                                        │ │
│  │ [View Details] [+ Add Observation]                    │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  [+ Create Standalone Observation]                         │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

**Key Features:**
- ✅ All AI-generated requirements visible
- ✅ Quick status overview (Compliant/Gap/Non-Compliant)
- ✅ Observation count per requirement
- ✅ Filter by risk level and status
- ✅ Add observations directly from requirement

---

### **Screen 2: Observation Capture (Mobile-Optimized)**

When auditor taps **"+ Add Observation"** on a requirement:

```
┌────────────────────────────────────────────────────────────┐
│  ← Back to Requirements                            [Save]  │
│  ────────────────────────────────────────────────────────  │
│                                                            │
│  📝 New Observation                                        │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ 📌 LINKED REQUIREMENT                                  │ │
│  │ ──────────────────────────────────────────────────────│ │
│  │ req_001 - CRITICAL                                     │ │
│  │ EU GMP Annex 1 § 4.29                                  │ │
│  │                                                        │ │
│  │ "When alert levels or action limits are exceeded,     │ │
│  │  investigate the cause..."                             │ │
│  │                                                        │ │
│  │ Expected Evidence:                                     │ │
│  │ • Investigation reports for all EM excursions          │ │
│  │ • CAPA records linked to excursions                    │ │
│  │ • Root cause analysis documentation                    │ │
│  │                                                        │ │
│  │ Common Gaps:                                           │ │
│  │ • Investigations not completed within timeframe        │ │
│  │ • Missing CAPA linkage for action limits               │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ 📝 YOUR OBSERVATION                                    │ │
│  │ ──────────────────────────────────────────────────────│ │
│  │                                                        │ │
│  │ What did you observe?                                  │ │
│  │ ┌────────────────────────────────────────────────────┐│ │
│  │ │ Reviewed EM data for March 2024. Found 3 action   ││ │
│  │ │ limit excursions in Grade A area. Investigation    ││ │
│  │ │ for EX-24-0312 was not completed within required   ││ │
│  │ │ 48-hour timeframe. Investigation report dated      ││ │
│  │ │ 5 days after excursion. No CAPA initiated.         ││ │
│  │ │                                                     ││ │
│  │ └────────────────────────────────────────────────────┘│ │
│  │                                                        │ │
│  │ [🎤 Voice Note] [📸 Photo] [📎 Attach Document]       │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  📍 Location: Grade A Filling Room 2                      │
│  👤 Interviewed: Sarah Chen (EM Coordinator)               │
│  📅 Date/Time: 2024-10-01 14:32                           │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ 🎯 COMPLIANCE STATUS                                   │ │
│  │ ──────────────────────────────────────────────────────│ │
│  │ ( ) ✓ Compliant - No issues found                     │ │
│  │ (•) ⚠️ Gap Identified - Minor deviation                │ │
│  │ ( ) ✗ Non-Compliant - Significant deviation           │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ 📎 EVIDENCE (3 items)                                  │ │
│  │ ──────────────────────────────────────────────────────│ │
│  │ 📸 IMG_20241001_1432.jpg                              │ │
│  │ 🎤 Voice note - 02:34                                 │ │
│  │ 📄 EM_Data_Mar2024.pdf                                │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  [🗑️ Discard]                          [💾 Save & Continue] │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

**Key Features:**
- ✅ **Requirement context always visible** - auditor sees what to look for
- ✅ **Expected evidence** from AI requirements guides observation
- ✅ **Common gaps** help auditor spot issues
- ✅ **Rich evidence capture** - text, voice, photo, documents
- ✅ **Compliance rating** - classify as compliant/gap/non-compliant
- ✅ **Auto-metadata** - location, interviewer, timestamp
- ✅ **Multi-modal input** - type, speak, or attach

---

### **Screen 3: Observation Detail View (Review Mode)**

```
┌────────────────────────────────────────────────────────────┐
│  ← Back to Requirements                    [Edit] [Delete] │
│  ────────────────────────────────────────────────────────  │
│                                                            │
│  ⚠️ OBSERVATION #OBS-001 - GAP IDENTIFIED                  │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ 📌 LINKED TO REQUIREMENT                               │ │
│  │ ──────────────────────────────────────────────────────│ │
│  │ req_001 - CRITICAL ⚠️                                  │ │
│  │ EU GMP Annex 1 § 4.29                                  │ │
│  │                                                        │ │
│  │ "When alert levels or action limits are exceeded,     │ │
│  │  there shall be an appropriate investigation..."       │ │
│  │                                                        │ │
│  │ [View Full Requirement Context]                        │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  📝 OBSERVATION                                            │
│  ──────────────────────────────────────────────────────── │
│  Reviewed EM data for March 2024. Found 3 action limit    │
│  excursions in Grade A area. Investigation for EX-24-0312  │
│  was not completed within required 48-hour timeframe.      │
│  Investigation report dated 5 days after excursion.        │
│  No CAPA initiated.                                        │
│                                                            │
│  🎯 COMPLIANCE ASSESSMENT                                  │
│  ──────────────────────────────────────────────────────── │
│  Status: ⚠️ GAP IDENTIFIED                                 │
│  Severity: MAJOR                                           │
│  Category: Quality System / Investigation Timeliness       │
│                                                            │
│  📎 EVIDENCE (3 items)                                     │
│  ──────────────────────────────────────────────────────── │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ 📸 EM Dashboard Screenshot                            │ │
│  │    IMG_20241001_1432.jpg                              │ │
│  │    [View] [Download]                                  │ │
│  └──────────────────────────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ 🎤 Interview with EM Coordinator                      │ │
│  │    Voice note - 02:34                                 │ │
│  │    "We had staffing issues that week and the          │ │
│  │     investigation got delayed..."                      │ │
│  │    [▶️ Play] [📝 Transcription]                        │ │
│  └──────────────────────────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ 📄 EM Excursion Data                                  │ │
│  │    EM_Data_Mar2024.pdf                                │ │
│  │    [View] [Download]                                  │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  ℹ️ METADATA                                               │
│  ──────────────────────────────────────────────────────── │
│  📍 Location: Grade A Filling Room 2                      │
│  👤 Auditor: John Smith                                    │
│  🗣️ Interviewed: Sarah Chen (EM Coordinator)              │
│  📅 Observed: October 1, 2024 at 2:32 PM                  │
│  📝 Last Updated: October 1, 2024 at 3:15 PM              │
│                                                            │
│  💭 NOTES & FOLLOW-UP                                      │
│  ──────────────────────────────────────────────────────── │
│  • Request trending data for past 6 months                │
│  • Check if SOP defines investigation timeframe           │
│  • Verify if similar delays in other areas                │
│                                                            │
│  [⬆️ Promote to Finding]        [📤 Share with Team]      │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

**Key Features:**
- ✅ **Full requirement context** one click away
- ✅ **Rich evidence display** - photos, audio with transcription
- ✅ **Compliance classification** visible
- ✅ **Complete metadata trail** for audit quality
- ✅ **Follow-up notes** for continuing investigation
- ✅ **Promote to finding** workflow integration

---

### **Screen 4: Requirement-Centric Review**

View all observations grouped by requirement:

```
┌────────────────────────────────────────────────────────────┐
│  🏭 Requirement Review - Environmental Monitoring          │
│  ────────────────────────────────────────────────────────  │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ 🔴 req_001 - CRITICAL                                  │ │
│  │ EU GMP Annex 1 § 4.29 - Investigation of Excursions    │ │
│  │                                                        │ │
│  │ When alert levels or action limits are exceeded,       │ │
│  │ there shall be an appropriate investigation to         │ │
│  │ determine the cause of the excursion. CAPA shall be    │ │
│  │ implemented when necessary.                            │ │
│  │                                                        │ │
│  │ ─────────────────────────────────────────────────────  │ │
│  │                                                        │ │
│  │ Expected Evidence:                                     │ │
│  │ ✓ Investigation reports for all EM excursions          │ │
│  │ ⚠️ CAPA records linked to excursions                   │ │
│  │ ✓ Root cause analysis documentation                    │ │
│  │ ⚠️ Trending reports showing EM performance             │ │
│  │                                                        │ │
│  │ ─────────────────────────────────────────────────────  │ │
│  │                                                        │ │
│  │ 📝 OBSERVATIONS (3)                                    │ │
│  │                                                        │ │
│  │ ┌────────────────────────────────────────────────────┐│ │
│  │ │ ⚠️ OBS-001 - GAP | Oct 1, 2:32 PM                  ││ │
│  │ │ Investigation EX-24-0312 completed 5 days late.    ││ │
│  │ │ No CAPA initiated for recurring issue.             ││ │
│  │ │ Evidence: 📸 2 photos | 🎤 1 audio | 📄 1 document  ││ │
│  │ │ [View Details]                                      ││ │
│  │ └────────────────────────────────────────────────────┘│ │
│  │                                                        │ │
│  │ ┌────────────────────────────────────────────────────┐│ │
│  │ │ ⚠️ OBS-002 - GAP | Oct 1, 3:45 PM                  ││ │
│  │ │ Trending analysis not performed quarterly as       ││ │
│  │ │ required by SOP-EM-001.                            ││ │
│  │ │ Evidence: 📸 1 photo | 📄 2 documents               ││ │
│  │ │ [View Details]                                      ││ │
│  │ └────────────────────────────────────────────────────┘│ │
│  │                                                        │ │
│  │ ┌────────────────────────────────────────────────────┐│ │
│  │ │ ✓ OBS-003 - COMPLIANT | Oct 1, 4:12 PM            ││ │
│  │ │ Recent excursion EX-24-0415 investigated within    ││ │
│  │ │ 24 hours. CAPA-2024-089 opened appropriately.      ││ │
│  │ │ Evidence: 📸 3 photos | 📄 1 document               ││ │
│  │ │ [View Details]                                      ││ │
│  │ └────────────────────────────────────────────────────┘│ │
│  │                                                        │ │
│  │ ─────────────────────────────────────────────────────  │ │
│  │                                                        │ │
│  │ 📊 COMPLIANCE SUMMARY                                  │ │
│  │ Status: ⚠️ PARTIAL COMPLIANCE - 2 GAPS IDENTIFIED      │ │
│  │                                                        │ │
│  │ Recommendation: CAPA required for investigation        │ │
│  │ timeliness and trending analysis processes.            │ │
│  │                                                        │ │
│  │ [+ Add Another Observation]   [Mark as Complete]      │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  [Next Requirement →]                                      │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

**Key Features:**
- ✅ **Requirement as central organizing principle**
- ✅ **All observations** for that requirement in one view
- ✅ **Evidence checklist** (expected vs. observed)
- ✅ **Quick status** for each observation
- ✅ **Summary recommendation** for report
- ✅ **Progressive disclosure** - summary with drill-down

---

## 🔄 Data Flow & Integration

### **Connection to AI Requirements**

```javascript
// When user creates observation from requirement
const observation = {
    id: "OBS-001",
    linkedRequirement: {
        id: "req_001",
        citation: "EU GMP Annex 1 § 4.29",
        text: "When alert levels...",
        expectedEvidence: [...],
        commonGaps: [...]
    },
    observationText: "Reviewed EM data...",
    complianceStatus: "gap", // compliant | gap | non-compliant
    severity: "major", // critical | major | minor
    evidence: [
        {type: "photo", url: "...", caption: "EM Dashboard"},
        {type: "audio", url: "...", transcription: "..."},
        {type: "document", url: "...", name: "EM_Data.pdf"}
    ],
    metadata: {
        location: "Grade A Filling Room 2",
        auditor: "John Smith",
        interviewed: "Sarah Chen",
        timestamp: "2024-10-01T14:32:00Z"
    },
    followUp: ["Request trending data", "Check SOP"]
}
```

### **Smart Features**

1. **Auto-Suggestions**
   - As auditor types observation, AI suggests which requirement it relates to
   - Pre-fills expected evidence checklist from requirement

2. **Evidence Matching**
   - AI compares captured evidence against "expected evidence" from requirement
   - Shows ✓ for matched, ⚠️ for missing

3. **Gap Detection**
   - Compares observation against "common gaps" from AI requirements
   - Auto-highlights potential issues

4. **Voice-to-Text**
   - Tap microphone, speak observation
   - Auto-transcribed and linked to requirement
   - Original audio preserved for review

---

## 📊 Analytics & Reporting

### **Real-Time Dashboard**

```
┌────────────────────────────────────────────────────────────┐
│  📊 Fieldwork Progress Dashboard                          │
│  ────────────────────────────────────────────────────────  │
│                                                            │
│  Requirements Coverage: ████████░░ 8/10 (80%)              │
│  Observations Captured: 23                                 │
│  Gaps Identified: 5                                        │
│                                                            │
│  Status Breakdown:                                         │
│  ✓ Compliant:        14 (61%)                             │
│  ⚠️ Gaps:             7 (30%)                             │
│  ✗ Non-Compliant:     2 (9%)                              │
│                                                            │
│  Evidence Collected:                                       │
│  📸 Photos: 45                                             │
│  🎤 Audio: 12                                              │
│  📄 Documents: 18                                          │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 💡 Key UX Principles

### **1. Requirement-Centric Design**
- Every observation is linked to a requirement (or marked standalone)
- Requirement context always available
- Expected evidence guides what to capture

### **2. Mobile-First**
- Thumb-friendly buttons
- Voice input for hands-free operation
- Offline-capable for facility walkdowns
- Auto-sync when back online

### **3. Rich Evidence**
- Multi-modal capture (text, voice, photo, document)
- In-line evidence preview
- Auto-metadata (location, time, interviewer)

### **4. Smart Assistance**
- AI suggests relevant requirements
- Pre-fills evidence checklist
- Highlights common gaps
- Auto-transcription of audio

### **5. Team Collaboration**
- Real-time sync across audit team
- Share observations instantly
- Collaborative review and editing
- Role-based access (lead auditor, team member, observer)

### **6. Quality Assurance**
- Required fields prevent incomplete observations
- Evidence requirements from AI ensure thoroughness
- Review mode before finalizing
- Audit trail of all changes

---

## 🎬 Complete User Journey Example

**Scenario:** Auditor John reviews Environmental Monitoring compliance

1. **Pre-Fieldwork:**
   - Reviews AI-generated req_001 (EM investigation timeliness)
   - Notes expected evidence: investigation reports, CAPA records
   - Notes common gaps: late investigations, missing CAPAs

2. **During Facility Walk:**
   - Opens mobile app in Grade A area
   - Taps "+ Observation" on req_001
   - Sees requirement context and expected evidence
   - Types observation: "Investigation EX-24-0312 completed 5 days late"
   - Takes photo of EM dashboard
   - Records voice note with EM coordinator
   - Marks status as "Gap - Major"
   - Saves (auto-syncs to cloud)

3. **Back at Desk:**
   - Reviews all observations on laptop
   - Sees 3 observations linked to req_001
   - Overall assessment: "Partial Compliance - 2 gaps"
   - Promotes OBS-001 and OBS-002 to formal findings
   - Generates recommendation: "CAPA required for investigation SOP"

4. **End of Day:**
   - Dashboard shows 23 observations across 8 requirements
   - 5 gaps requiring CAPA
   - All evidence securely stored
   - Ready for report generation

---

## 🚀 Implementation Benefits

✅ **Consistency** - Every observation has requirement context  
✅ **Completeness** - Expected evidence ensures thorough audits  
✅ **Efficiency** - Voice input speeds capture 3x  
✅ **Quality** - AI-guided gap detection improves accuracy  
✅ **Traceability** - Full audit trail from requirement → observation → finding  
✅ **Collaboration** - Real-time team sync  
✅ **Reporting** - One-click export to final report  

---

**Next Steps:**
1. Build observation capture UI
2. Integrate voice-to-text
3. Create requirement-observation linking logic
4. Implement evidence management system
5. Build analytics dashboard

