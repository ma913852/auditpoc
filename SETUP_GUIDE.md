# Audit POC - LLM Integration Setup Guide

## Overview
This implementation uses **Databricks Claude Sonnet 3.5** to intelligently generate regulatory compliance requirements based on your audit scope.

## Architecture

```
┌─────────────────┐         ┌──────────────┐         ┌─────────────────────┐
│   Frontend      │         │   Backend    │         │   Databricks        │
│  (audit_poc.html)│ ──────> │  Flask API   │ ──────> │  Claude Sonnet 3.5  │
│                 │         │   (app.py)   │         │                     │
└─────────────────┘         └──────────────┘         └─────────────────────┘
```

## Setup Instructions

### 1. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Databricks Access

Create a `.env` file in the project root:

```bash
DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
DATABRICKS_TOKEN=dapi1234567890abcdef...
```

**How to get your Databricks token:**
1. Log into your Databricks workspace
2. Go to User Settings → Developer → Access Tokens
3. Click "Generate New Token"
4. Copy the token and add it to your `.env` file

### 3. Verify Model Endpoint

The default endpoint is:
```
/serving-endpoints/databricks-claude-sonnet3-7/invocations
```

If your endpoint is different, update it in `app.py` (around line 35).

### 4. Start the Server

```bash
python app.py
```

The server will start on `http://localhost:5000` with both the frontend and API endpoints.

### 5. Open the Frontend

Navigate to `http://localhost:5000` in your browser. The server hosts both the frontend and API.

## Usage Flow

1. **Define Audit Scope**: Fill in the Audit Scope & Standards section (or use existing data)
2. **Generate Requirements**: Click the "Generate Requirements" button
3. **View Results**: Browse requirements by category, view details, and export

## How It Works

### 1. Data Collection
The frontend JavaScript collects audit scope data:
- Facility information
- Process areas
- Products
- Time period
- Key systems
- Regulatory framework

### 2. API Call
Data is sent to the Flask backend via POST request:

```javascript
fetch('http://localhost:5000/api/generate-requirements', {
    method: 'POST',
    body: JSON.stringify(auditScope)
})
```

### 3. LLM Processing
Backend calls Databricks Claude Sonnet 3.5 with a specialized prompt:

```python
response = requests.post(
    f"{DATABRICKS_HOST}/serving-endpoints/databricks-claude-sonnet3-7/invocations",
    headers={"Authorization": f"Bearer {DATABRICKS_TOKEN}"},
    json={
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3  # Low temp for consistent output
    }
)
```

### 4. Response Parsing
The LLM returns structured JSON with:
- **Categories**: Environmental Monitoring, Training, Documentation, etc.
- **Requirements**: Each with citation, risk level, evidence needed
- **Audit Focus**: Specific areas to examine during the audit

### 5. UI Display
Requirements are displayed with:
- Category filtering
- Risk-level badges (Critical, High, Medium, Low)
- Expandable details (compliance evidence, common gaps)
- Export functionality

## Example Response Structure

```json
{
  "total_requirements": 45,
  "categories": [
    {
      "category_name": "Environmental Monitoring",
      "requirement_count": 8,
      "requirements": [
        {
          "id": "req_001",
          "citation": "EU GMP Annex 1 § 4.29",
          "regulation_name": "EU GMP Annex 1 (2022)",
          "category": "Environmental Monitoring",
          "requirement_text": "When alert levels or action limits are exceeded...",
          "risk_level": "Critical",
          "compliance_evidence": [
            "Investigation reports for all EM excursions",
            "CAPA records linked to excursions"
          ],
          "common_gaps": [
            "Investigations not completed within defined timeframe"
          ],
          "audit_focus": "Review EM excursions from the past 12 months"
        }
      ]
    }
  ]
}
```

## Customization

### Adjust Temperature
In `app.py`, modify the `temperature` parameter in the `call_claude()` function (around line 83):
- **Lower (0.1-0.3)**: More focused, consistent output
- **Higher (0.7-1.0)**: More creative, varied output

### Modify Prompt
Customize the prompt in the `build_requirements_prompt()` function in `app.py` to:
- Focus on specific regulatory areas
- Add industry-specific context
- Adjust requirement depth

### Change UI Theme
Update Tailwind classes in `audit_poc.html` to match your branding.

## Troubleshooting

### Connection Errors
If you can't connect to the API:
- Ensure the server is running: `python app.py`
- Verify you're accessing `http://localhost:5000`
- Check the console for error messages

### API Timeout
If the LLM call times out:
- Check your Databricks token is valid
- Verify the endpoint URL is correct
- Increase timeout in `app.py` in the `call_claude()` function (around line 87)

### Empty Response
If no requirements are generated:
- Check the browser console for errors
- Verify audit scope fields are populated
- Review backend logs for parsing errors

## Production Deployment

For production use:
1. **Environment Variables**: Use proper secrets management
2. **HTTPS**: Enable SSL/TLS
3. **Rate Limiting**: Add rate limiting to API endpoints
4. **Caching**: Cache LLM responses to reduce costs
5. **Monitoring**: Add logging and error tracking

## Cost Optimization

- **Cache Results**: Store generated requirements by audit scope hash
- **Batch Processing**: Generate requirements for multiple audits at once
- **Prompt Optimization**: Refine prompts to reduce token usage
- **Streaming**: Use streaming endpoint for real-time updates (see `api_server.py`)

## Next Steps

1. **RAG Integration**: Connect uploaded documents to enrich requirement generation
2. **Gap Analysis**: Compare generated requirements against actual audit findings
3. **Export Formats**: Add PDF, Excel export options
4. **Collaboration**: Multi-user editing and commenting

## Support

For issues or questions:
- Check Databricks documentation: https://docs.databricks.com/
- Review Flask API logs
- Inspect browser console for frontend errors

