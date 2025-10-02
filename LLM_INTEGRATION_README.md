# LLM Integration - Quick Start 🚀

## What's New

Your Audit POC now includes **AI-powered requirement generation** using **Databricks Claude Sonnet 3.5**!

The system analyzes your audit scope and automatically generates 30-50 specific, actionable compliance requirements tailored to your facility, process areas, and regulatory framework.

## Files Modified/Created

```
audit poc/
├── app.py                    # Main Flask server (LLM functionality integrated)
├── requirements.txt          # Python dependencies (updated)
├── test_llm_endpoint.py      # Test script
├── start_server.bat         # Windows startup script
├── audit_poc.html           # Frontend (AI requirements section added)
├── SETUP_GUIDE.md           # Detailed documentation
└── LLM_INTEGRATION_README.md # This file
```

## Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements_backend.txt
```

### Step 2: Configure Databricks
Create a `.env` file in the project root:

```
DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
DATABRICKS_TOKEN=dapi1234567890abcdef...
```

### Step 3: Start the Server

**Windows:**
```bash
start_server.bat
```

**Mac/Linux:**
```bash
python app.py
```

## Test It Works

```bash
python test_llm_endpoint.py
```

This will verify your setup and generate sample requirements.

## How to Use in the UI

1. Open `audit_poc.html` in your browser
2. Navigate to **Audit Scope & Standards** section
3. Click the **"Generate Requirements"** button (purple/blue gradient)
4. Wait 15-30 seconds while Claude analyzes your scope
5. Browse requirements by category, view details, and export!

## Features

### ✨ Smart Generation
- Analyzes your facility, process areas, and products
- Focuses on relevant regulations (FDA, EU GMP, etc.)
- Prioritizes critical requirements

### 🏷️ Categorized Output
- Environmental Monitoring
- Training & Qualification
- Documentation & Records
- Equipment & Facilities
- Validation & Verification
- Quality Systems

### 📊 Rich Details
Each requirement includes:
- **Citation** (e.g., "21 CFR 211.113")
- **Risk Level** (Critical, High, Medium, Low)
- **Compliance Evidence** needed
- **Common Gaps** to watch for
- **Audit Focus** areas

### 🎯 Interactive UI
- Filter by category
- Expand/collapse details
- Risk-level color coding
- Export to JSON

## API Endpoints

### Health Check
```bash
GET http://localhost:5000/api/health
```

### Generate Requirements
```bash
POST http://localhost:5000/api/generate-requirements
Content-Type: application/json

{
  "facility": "PharmaCore Site C - Aseptic Filling Suite 2",
  "process_areas": ["Grade A/B Aseptic Filling"],
  "products": "Injectable biologics",
  "time_period": "January 2024 - December 2024",
  "key_systems": ["QMS", "Training System"],
  "regulatory_requirements": ["FDA 21 CFR Part 211", "EU GMP Annex 1"]
}
```

## Troubleshooting

### "Cannot connect to API server"
→ Make sure the backend is running: `python api_server.py`

### "API error: 401" or "Unauthorized"
→ Check your Databricks token in `.env` file

### "API error: 404"
→ Verify your model endpoint URL in `api_server.py`

### CORS errors in browser
→ Ensure `flask-cors` is installed and the server is running on localhost:5000

## Architecture

```
User fills Audit Scope
      ↓
Frontend collects data
      ↓
POST to /api/generate-requirements
      ↓
Backend builds specialized prompt
      ↓
Calls Databricks Claude Sonnet 3.5
      ↓
Parses structured JSON response
      ↓
Returns requirements to frontend
      ↓
UI displays with filtering & export
```

## Customization

### Change Model Temperature
Lower = more consistent, Higher = more creative

In `app.py` (around line 83):
```python
"temperature": 0.3  # Adjust between 0.1 - 1.0
```

### Modify Prompt
Edit the `build_requirements_prompt()` function in `app.py` to:
- Focus on specific regulatory areas
- Add industry context
- Adjust requirement depth

### Update UI Theme
Modify Tailwind classes in `audit_poc.html` around line 193-263

## What's Next?

Potential enhancements:
1. **RAG Integration**: Use uploaded documents to enrich requirements
2. **Gap Analysis**: Compare requirements against audit findings
3. **PDF Export**: Export requirements as formatted PDF
4. **Caching**: Cache results to reduce API calls
5. **Batch Processing**: Generate requirements for multiple audits

## Cost Considerations

Each generation uses:
- ~2,000 input tokens (prompt)
- ~15,000-25,000 output tokens (response)

Databricks Claude Sonnet 3.5 pricing:
- Input: ~$3 per million tokens
- Output: ~$15 per million tokens

**Estimated cost per generation: $0.38 - $0.63**

💡 **Tip**: Cache results by audit scope hash to avoid regenerating identical requirements!

## Support

Need help?
- See detailed docs: `SETUP_GUIDE.md`
- Check API logs for backend errors
- Inspect browser console for frontend issues
- Review Databricks endpoint status

---

**Happy Auditing! 🎯**

