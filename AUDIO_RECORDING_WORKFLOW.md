# 🎤 Audio Recording Implementation - Complete Workflow

## Overview

The audio recording feature allows users to capture voice notes during fieldwork observations. The recording is done using the browser's **MediaRecorder API** and integrated with AI analysis.

---

## 🏗️ Architecture

```
User Interface (HTML)
        ↓
JavaScript MediaRecorder API
        ↓
Audio Blob (WebM format)
        ↓
User adds transcription (manual or AI)
        ↓
Sent to backend for AI analysis
        ↓
AI matches to requirements
```

---

## 📋 Components

### **1. HTML Elements**

```html
<!-- Record Button -->
<button id="recordBtn" onclick="toggleRecording()" 
        class="w-full px-3 py-2 bg-red-500 text-white rounded-lg">
    🎤 <span id="recordBtnText">Record</span>
</button>

<!-- Audio Preview (shows while recording) -->
<div id="audioPreview" class="hidden mt-2 p-2 bg-slate-50 rounded">
    🎤 <span id="recordDuration">0:00</span>
</div>

<!-- Transcription Textarea (appears after recording) -->
<textarea id="audioTranscription" 
          placeholder="Transcription..." 
          class="hidden" rows="2">
</textarea>
```

### **2. State Variables**

```javascript
let mediaRecorder = null;           // MediaRecorder instance
let audioChunks = [];              // Stores audio data chunks
let capturedAudio = null;          // Blob URL of recorded audio
let recordingStartTime = null;     // When recording started
let recordingInterval = null;      // Timer interval for duration display
```

---

## 🔄 Complete Workflow

### **STEP 1: User Clicks "Record" Button**

```
User clicks: 🎤 Record
      ↓
toggleRecording() is called
      ↓
Checks: Is mediaRecorder inactive?
      ↓ YES
Request microphone permission
```

### **STEP 2: Request Microphone Permission**

```javascript
const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
```

**What happens:**
- Browser shows permission prompt
- User grants/denies microphone access
- If granted: Returns MediaStream
- If denied: Throws error → Shows alert

### **STEP 3: Initialize MediaRecorder**

```javascript
mediaRecorder = new MediaRecorder(stream);
audioChunks = [];  // Reset chunks array
```

**Set up event handlers:**

```javascript
// When data is available, store it
mediaRecorder.ondataavailable = (event) => {
    audioChunks.push(event.data);
};

// When recording stops
mediaRecorder.onstop = () => {
    // Create audio blob from chunks
    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
    
    // Create URL for playback (if needed)
    capturedAudio = URL.createObjectURL(audioBlob);
    
    // Show transcription field
    document.getElementById('audioPreview').classList.remove('hidden');
    document.getElementById('audioTranscription').classList.remove('hidden');
    document.getElementById('audioTranscription').value = 
        "[Audio recorded - type transcription or let AI analyze]";
    
    // Stop all tracks (release microphone)
    stream.getTracks().forEach(track => track.stop());
    
    // Stop duration timer
    clearInterval(recordingInterval);
};
```

### **STEP 4: Start Recording**

```javascript
mediaRecorder.start();
recordingStartTime = Date.now();

// Update UI
btn.classList.add('recording');  // Adds pulsing red animation
btnText.innerText = 'Stop Recording';

// Start duration timer (updates every second)
recordingInterval = setInterval(() => {
    const elapsed = Math.floor((Date.now() - recordingStartTime) / 1000);
    const minutes = Math.floor(elapsed / 60);
    const seconds = elapsed % 60;
    document.getElementById('recordDuration').innerText = 
        `${minutes}:${seconds.toString().padStart(2, '0')}`;
}, 1000);
```

**Visual feedback:**
```
🎤 Stop Recording  ← Button pulses red
🎤 Recording: 0:15  ← Live duration counter
```

### **STEP 5: User Clicks "Stop Recording"**

```javascript
else {
    mediaRecorder.stop();  // Triggers onstop event
    btn.classList.remove('recording');
    btnText.innerText = 'Start Recording';
}
```

**What happens:**
1. `mediaRecorder.stop()` is called
2. Triggers `onstop` event handler
3. Audio chunks are combined into Blob
4. Transcription field appears
5. Microphone is released
6. Timer stops

### **STEP 6: User Adds Transcription (Optional)**

```
User can:
1. Type transcription manually
2. Leave placeholder text
3. Let AI analyze the audio content
```

### **STEP 7: AI Analysis**

When user clicks "⚡ Analyze with AI":

```javascript
async function analyzeWithAI() {
    const obsText = document.getElementById('obsText').value.trim();
    const imageDesc = document.getElementById('imageDescription').value.trim();
    const audioTrans = document.getElementById('audioTranscription').value.trim();
    
    // Send to backend
    const response = await fetch('/api/observations/analyze', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            observationText: obsText,
            imageDescription: imageDesc,
            audioTranscription: audioTrans,  // ← Audio transcription sent here
            requirements: fieldworkRequirements
        })
    });
    
    const result = await response.json();
    
    if (result.success) {
        // Display AI's matched requirement
        displayRequirementMatch(result.analysis);
    }
}
```

### **STEP 8: Backend Processing**

Backend receives:
```json
{
  "observationText": "Investigation was delayed...",
  "imageDescription": "",
  "audioTranscription": "The supervisor mentioned they were short-staffed",
  "requirements": [...]
}
```

AI analyzes all inputs together and returns:
```json
{
  "matched_requirements": [{
    "requirement_id": "req_001",
    "confidence": 0.95,
    "reasoning": "Investigation delay mentioned in text and confirmed in audio"
  }],
  "key_findings": [...],
  "compliance_status": "non_compliant",
  "severity": "major"
}
```

### **STEP 9: Clear Audio (Optional)**

User can clear the recording:

```javascript
function clearAudio() {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
    }
    
    capturedAudio = null;
    audioChunks = [];
    
    // Hide UI elements
    document.getElementById('audioPreview').classList.add('hidden');
    document.getElementById('audioTranscription').classList.add('hidden');
    document.getElementById('audioTranscription').value = '';
    
    // Reset button
    document.getElementById('recordBtn').classList.remove('recording');
    document.getElementById('recordBtnText').innerText = 'Start Recording';
}
```

---

## 🎨 Visual States

### **State 1: Initial (Not Recording)**
```
┌─────────────────────────┐
│ 🎤 Voice (Optional)     │
│ [🎤 Record]             │
└─────────────────────────┘
```

### **State 2: Recording**
```
┌─────────────────────────┐
│ 🎤 Voice (Optional)     │
│ [🎤 Stop Recording] ←pulsing red
│ 🎤 Recording: 0:15      │
└─────────────────────────┘
```

### **State 3: Recorded**
```
┌─────────────────────────┐
│ 🎤 Voice (Optional)     │
│ [🎤 Record]             │
│ 🎤 Recording: 0:15      │
│ [Transcription...]      │
└─────────────────────────┘
```

---

## 🔧 Technical Details

### **Audio Format**
- **Container:** WebM (browser default)
- **Codec:** Opus (most common)
- **MIME Type:** `audio/webm`

### **Browser Support**
- ✅ Chrome/Edge: Full support
- ✅ Firefox: Full support  
- ✅ Safari: Limited support (may need polyfill)
- ❌ IE11: Not supported

### **Permissions**
- Requires HTTPS (except localhost)
- User must grant microphone permission
- Permission persists for the session
- Can be revoked by user at any time

### **Storage**
Currently: **In-memory only**
- Audio blob stored in browser memory
- Lost on page refresh
- Not sent to server (only transcription is sent)

**Future enhancement:** Upload audio file to server for:
- Server-side transcription (Whisper API)
- Audio evidence storage
- Playback in observation details

---

## 🚀 Workflow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    USER JOURNEY                         │
└─────────────────────────────────────────────────────────┘

1. User clicks "🎤 Record"
          ↓
2. Browser asks for microphone permission
          ↓
3. User grants permission
          ↓
4. Recording starts
   - Button changes to "Stop Recording"
   - Button pulses red
   - Timer shows: "🎤 Recording: 0:00"
   - Timer increments every second
          ↓
5. User observes/speaks (e.g., 15 seconds)
          ↓
6. User clicks "🎤 Stop Recording"
          ↓
7. Recording stops
   - Audio chunks → Blob → URL
   - Transcription field appears
   - Microphone released
   - Timer stops
          ↓
8. User types transcription (or leaves placeholder)
          ↓
9. User clicks "⚡ Analyze with AI"
          ↓
10. Audio transcription sent to backend with observation text
          ↓
11. AI analyzes combined inputs (text + audio + image)
          ↓
12. AI returns matched requirement + insights
          ↓
13. User reviews and saves observation
```

---

## 📝 Code Flow Summary

```javascript
// 1. INITIALIZE (on page load)
let mediaRecorder = null;
let audioChunks = [];
let capturedAudio = null;

// 2. START RECORDING (user clicks Record)
toggleRecording() {
    ↓
  getUserMedia({ audio: true })
    ↓
  mediaRecorder = new MediaRecorder(stream)
    ↓
  mediaRecorder.start()
    ↓
  Update UI (button, timer)
}

// 3. STOP RECORDING (user clicks Stop)
toggleRecording() {
    ↓
  mediaRecorder.stop()
    ↓
  onstop event fires
    ↓
  Combine chunks → Blob
    ↓
  Show transcription field
    ↓
  Release microphone
}

// 4. ANALYZE (user clicks Analyze with AI)
analyzeWithAI() {
    ↓
  Get audioTranscription value
    ↓
  Send to /api/observations/analyze
    ↓
  Display AI results
}

// 5. CLEAR (user clicks Clear)
clearAudio() {
    ↓
  Stop recording if active
    ↓
  Reset all variables
    ↓
  Hide UI elements
}
```

---

## 🐛 Error Handling

### **Permission Denied**
```javascript
catch (error) {
    console.error('Microphone error:', error);
    alert('Could not access microphone. Please grant permission.');
}
```

**Common reasons:**
- User clicked "Block" on permission prompt
- Browser doesn't support MediaRecorder API
- HTTPS not enabled (except localhost)
- Microphone already in use by another app

### **Recording Fails**
- Browser compatibility check
- Fallback to manual transcription
- Clear error messages to user

---

## 🔮 Future Enhancements

### **1. Server-Side Transcription**
```javascript
// Upload audio file to server
const formData = new FormData();
formData.append('audio', audioBlob, 'recording.webm');

await fetch('/api/transcribe', {
    method: 'POST',
    body: formData
});

// Backend uses Whisper API
// Returns transcription automatically
```

### **2. Audio Playback**
```javascript
// Add play button to review recording
<audio controls src={capturedAudio}>
    Your browser does not support audio playback.
</audio>
```

### **3. Real-Time Transcription**
```javascript
// Use Web Speech API for live transcription
const recognition = new webkitSpeechRecognition();
recognition.continuous = true;
recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    document.getElementById('audioTranscription').value = transcript;
};
```

### **4. Audio Analysis**
- Sentiment analysis (tone, urgency)
- Speaker identification
- Keyword extraction
- Confidence scoring

---

## ✅ Summary

**Current Implementation:**
- ✅ Browser-based recording using MediaRecorder API
- ✅ WebM format (Opus codec)
- ✅ In-memory storage (blob URL)
- ✅ Manual transcription field
- ✅ Transcription sent to AI for analysis
- ✅ Visual feedback (pulsing button, timer)
- ✅ Error handling (permission denied)

**Not Implemented (Yet):**
- ❌ Server-side audio file upload
- ❌ Automatic transcription (Whisper API)
- ❌ Audio playback in UI
- ❌ Persistent storage
- ❌ Audio analysis/sentiment detection

**Simple & Effective:**
The current implementation provides a streamlined way to capture voice notes with minimal complexity. Audio transcription is sent to AI along with observation text for comprehensive analysis.

---

## 🎯 Key Takeaway

The audio recording is **client-side only** (browser API), captures voice as **WebM blob**, allows user to add **manual transcription**, and sends **transcription text** (not audio file) to backend for **AI analysis** alongside observation text and image description.

**Flow:** Record → Transcribe → Analyze → Match to Requirement → Save

