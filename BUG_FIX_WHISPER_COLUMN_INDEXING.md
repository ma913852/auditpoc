# 🐛 Bug Fix: Whisper Column Indexing

## Issue

```
HTTP error from Whisper API: 400 - {"error_code": "BAD_REQUEST", 
"message": "Failed to enforce schema of data with schema '[0: binary (required)]'. 
Error: Model is missing inputs [0]. Note that there were extra inputs: ['audio']"}
```

---

## Root Cause

The Whisper model endpoint expects **positional indexing** for columns, not named columns.

### **What We Sent (Wrong):**
```python
payload = {
    "dataframe_split": {
        "columns": ["audio"],  # ❌ Named column
        "data": [[audio_base64]]
    }
}
```

### **What Whisper Expected:**
```python
payload = {
    "dataframe_split": {
        "columns": [0],  # ✅ Positional index
        "data": [[audio_base64]]
    }
}
```

---

## Error Analysis

The error message tells us:
- **"Model is missing inputs [0]"** - Expects input at position `[0]`
- **"There were extra inputs: ['audio']"** - Found column named `'audio'` instead
- **"schema '[0: binary (required)]'"** - Schema defines position `0` as binary

This indicates the Whisper model was trained/deployed with **positional column indexing** rather than named columns.

---

## Solution

Changed the `columns` field from a string `["audio"]` to an integer `[0]`:

```python
# Define the JSON payload in dataframe_split format
# Use positional indexing (0) instead of column names
payload = {
    "dataframe_split": {
        "columns": [0],  # ✅ Changed from ["audio"] to [0]
        "data": [[audio_base64]]
    }
}
```

---

## Code Changes

### **app.py (Lines 814-821)**

**Before:**
```python
# Define the JSON payload in dataframe_split format
payload = {
    "dataframe_split": {
        "columns": ["audio"],  # ❌ Wrong
        "data": [[audio_base64]]
    }
}
```

**After:**
```python
# Define the JSON payload in dataframe_split format
# Use positional indexing (0) instead of column names
payload = {
    "dataframe_split": {
        "columns": [0],  # ✅ Fixed
        "data": [[audio_base64]]
    }
}
```

---

## Understanding Dataframe Split Format

### **Format 1: Named Columns** (Used by some models)
```python
{
    "dataframe_split": {
        "columns": ["input_text", "temperature"],
        "data": [["Hello world", 0.7]]
    }
}
```

### **Format 2: Positional Indexing** (Used by Whisper)
```python
{
    "dataframe_split": {
        "columns": [0, 1],  # Positional indices
        "data": [[audio_base64, "en"]]  # Values at positions 0, 1
    }
}
```

For Whisper with single input:
```python
{
    "dataframe_split": {
        "columns": [0],  # Single position
        "data": [[audio_base64]]  # Single value
    }
}
```

---

## Why This Matters

Databricks model serving endpoints can be configured with different input schemas:

1. **Schema with named features:**
   - Columns: `["audio"]`
   - Used when model signature has named inputs

2. **Schema with positional features:**
   - Columns: `[0]`
   - Used when model signature uses position-based inputs
   - More common for models converted from other frameworks

The Whisper model was deployed with a positional schema: `[0: binary (required)]`

---

## Testing

### **Test Request**
```python
import requests
import base64

# Read audio
with open("test.webm", "rb") as f:
    audio_base64 = base64.b64encode(f.read()).decode("utf-8")

# Build payload with positional indexing
payload = {
    "dataframe_split": {
        "columns": [0],  # ✅ Positional
        "data": [[audio_base64]]
    }
}

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

response = requests.post(whisper_url, headers=headers, json=payload)
print(response.json())
```

### **Expected Response**
```json
{
    "predictions": [
        "During the batch record review, I found that..."
    ]
}
```

---

## Verification

### **Before Fix:**
```bash
❌ HTTP 400 - BAD_REQUEST
❌ "Model is missing inputs [0]"
❌ "There were extra inputs: ['audio']"
```

### **After Fix:**
```bash
✅ HTTP 200 - OK
✅ Transcription successful
✅ Audio correctly transcribed
```

---

## Related Documentation

Update all examples in documentation to use positional indexing:

### **AUDIO_TRANSCRIPTION_IMPLEMENTATION.md**
```python
# ✅ Correct format
payload = {
    "dataframe_split": {
        "columns": [0],
        "data": [[audio_base64]]
    }
}
```

### **WHISPER_DATAFRAME_SPLIT_UPDATE.md**
```python
# ✅ Correct format
payload = {
    "dataframe_split": {
        "columns": [0],  # Not ["audio"]
        "data": [[audio_base64]]
    }
}
```

---

## Lessons Learned

1. **Check model schema** - Different models may use named or positional columns
2. **Read error messages carefully** - "missing inputs [0]" is a clue about positional indexing
3. **Test with sample data** - Validate payload format before integration
4. **Document model requirements** - Note whether columns are named or positional

---

## How to Identify Column Format

When working with a new Databricks endpoint:

1. **Check endpoint documentation** for input schema
2. **Look for error messages** mentioning `[0]`, `[1]`, etc. (positional)
3. **Try both formats** if documentation is unclear
4. **Use positional by default** for binary inputs like audio/images

---

## Summary

**Issue:** Whisper API expected positional column indexing `[0]` but received named column `["audio"]`

**Fix:** Changed `"columns": ["audio"]` to `"columns": [0]`

**Impact:** Audio transcription now works correctly with the Whisper endpoint

---

## Status

✅ **RESOLVED** - Whisper transcription now uses correct positional column indexing and successfully transcribes audio files.

