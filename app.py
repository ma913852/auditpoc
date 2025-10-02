from flask import Flask, request, jsonify, send_file, send_from_directory
import os
import uuid
from datetime import datetime
import mimetypes
from werkzeug.utils import secure_filename
from openai import OpenAI
import json
import base64
import requests
from dotenv import load_dotenv

# Load environment variables for Databricks
load_dotenv(r'C:\Users\ma913852\OneDrive - BioMarin\Documents\projects\env_audit_poc.example')  # Specify the file path

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
AUDIO_FOLDER = 'audio_uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
ALLOWED_AUDIO_EXTENSIONS = {'webm', 'wav', 'mp3', 'ogg', 'm4a'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_AUDIO_SIZE = 50 * 1024 * 1024  # 50MB

# Ensure upload directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_AUDIO_SIZE

# Databricks Configuration
DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")
WHISPER_HOST = os.getenv("WHISPER_HOST")

# Initialize OpenAI client for Databricks Claude
client = OpenAI(
    api_key=DATABRICKS_TOKEN,
    base_url=DATABRICKS_HOST
)

# Note: Whisper uses direct HTTP requests with dataframe_split format
# No separate client initialization needed

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_audio_file(filename):
    """Check if audio file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_AUDIO_EXTENSIONS

def get_file_size_mb(file_path):
    """Get file size in MB"""
    return round(os.path.getsize(file_path) / (1024 * 1024), 1)

def generate_thumbnail_path(file_path):
    """Generate thumbnail path for document preview"""
    # In a real application, you would generate actual thumbnails
    # For now, we'll return placeholder URLs
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    ext = os.path.splitext(file_path)[1].lower()
    
    # Generate different colored placeholders based on file type
    colors = {
        '.pdf': '0D47A1',
        '.doc': '2D3748', 
        '.docx': '4A5568'
    }
    
    color = colors.get(ext, '718096')
    return f"https://placehold.co/300x400/{color}/FFFFFF?text={base_name.replace(' ', '+')}"

# ============================================================================
# LLM REQUIREMENT GENERATION FUNCTIONS
# ============================================================================

def call_claude(prompt, max_tokens=40000):
    """Call Databricks Claude Sonnet 4 using OpenAI-compatible API"""
    print (prompt)
    try:
        response = client.chat.completions.create(
            model="databricks-claude-sonnet-4",  # Databricks model name
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.3,  # Lower temperature for consistent output
            timeout=60
        )
        print (response.choices[0].message.content)
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error calling Databricks Claude via OpenAI client: {e}")
        raise

def call_claude_with_vision(prompt, image_base64, max_tokens=4000):
    """
    Call Databricks Claude Sonnet 4 with vision capabilities (single image)
    
    Args:
        prompt: Text prompt for analysis
        image_base64: Base64-encoded image string (with or without data URI prefix)
        max_tokens: Maximum tokens in response
    
    Returns:
        Claude's response as string
    """
    return call_claude_with_multiple_images(prompt, [image_base64], max_tokens)

def call_claude_with_multiple_images(prompt, images_base64, max_tokens=4000):
    """
    Call Databricks Claude Sonnet 4 with vision capabilities (multiple images)
    
    Args:
        prompt: Text prompt for analysis
        images_base64: List of Base64-encoded image strings (with or without data URI prefix)
        max_tokens: Maximum tokens in response
    
    Returns:
        Claude's response as string
    """
    try:
        if not images_base64:
            raise ValueError("No images provided")
        
        # Build content array with all images and text
        content = []
        
        # Add all images first
        for idx, image_base64 in enumerate(images_base64):
            # Extract base64 data from data URI if present
            if image_base64.startswith('data:'):
                # Format: data:image/jpeg;base64,/9j/4AAQSkZJRg...
                header, encoded = image_base64.split(',', 1)
                # Extract media type
                media_type = header.split(';')[0].split(':')[1]  # e.g., "image/jpeg"
            else:
                encoded = image_base64
                media_type = "image/jpeg"  # Default
            
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:{media_type};base64,{encoded}"
                }
            })
            
            print(f"Image {idx+1}: {len(encoded)} bytes, {media_type}")
        
        # Add text prompt last
        content.append({
            "type": "text",
            "text": prompt
        })
        
        print(f"Calling Claude with vision... {len(images_base64)} image(s)")
        
        # Use Anthropic message format with vision
        # The OpenAI client for Databricks should support this format
        response = client.chat.completions.create(
            model="databricks-claude-sonnet-4",
            messages=[{
                "role": "user",
                "content": content
            }],
            max_tokens=max_tokens,
            temperature=0.3,
            timeout=120  # Longer timeout for multiple images
        )
        
        response_text = response.choices[0].message.content
        print(f"Claude vision response received ({len(response_text)} chars)")
        return response_text
        
    except Exception as e:
        print(f"Error calling Claude with vision: {e}")
        import traceback
        print(traceback.format_exc())
        raise

def build_requirements_prompt(audit_scope):
    """Build specialized prompt for Claude based on audit scope"""
    facility = audit_scope.get('facility', 'Not specified')
    process_areas = audit_scope.get('process_areas', [])
    products = audit_scope.get('products', 'Not specified')
    time_period = audit_scope.get('time_period', 'Not specified')
    key_systems = audit_scope.get('key_systems', [])
    regulatory_reqs = audit_scope.get('regulatory_requirements', [])
    
    prompt = f"""You are a GxP regulatory compliance expert specializing in pharmaceutical audits. 
Based on the following audit scope, generate a comprehensive list of specific regulatory requirements 
that must be verified during this audit.

AUDIT SCOPE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Facility: {facility}

Process Areas:
{chr(10).join(f"• {area}" for area in process_areas) if process_areas else "• Not specified"}

Products in Scope: {products}

Time Period: {time_period}

Key Systems:
{chr(10).join(f"• {system}" for system in key_systems) if key_systems else "• Not specified"}

Regulatory Framework:
{chr(10).join(f"• {req}" for req in regulatory_reqs) if regulatory_reqs else "• FDA 21 CFR Part 211, EU GMP Annex 1"}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TASK:
Generate 10 specific, actionable regulatory requirements that apply to this audit scope.
Focus on requirements most relevant to the identified process areas and products.

For each requirement, provide:
1. A unique identifier
2. The regulatory citation (e.g., "21 CFR 211.113" or "EU GMP Annex 1 § 4.29")
3. The category (e.g., "Environmental Monitoring", "Training", "Documentation")
4. The specific requirement text
5. Risk level (Critical, High, Medium, Low)
6. What evidence would demonstrate compliance and suggested document asked for in the evidence
7. Common gaps or findings related to this requirement


Organize requirements by category for clarity.

CRITICAL: Respond ONLY with valid JSON. No text before or after the JSON.
No trailing commas. Ensure all strings are properly escaped.

Use this EXACT format:
{{
  "requirements": [
    {{
      "id": "req_001",
      "regulation_name": "21 CFR 211.42",
      "category": "Environmental Monitoring",
      "requirement_text (verbatim)": "When alert or action levels are exceeded, investigations must be initiated immediately. **21 CFR 211.42(c)(10)(iv)**",
      "risk_level": "Critical",
      "compliance_evidence": [
        "EM data review",
        "Investigation reports",
        "CAPA records",
        "Trending analysis"
      ],
      "common_gaps": [
        "Delayed investigation initiation",
        "Incomplete root cause analysis",
        "Missing CAPA linkage",
        "Inadequate trending"
      ],
      "suggested_audit_focus": "Review EM excursions from past 12 months and verify investigation completeness"
    }}
  ]
}}



Generate requirements that are:
- Specific to the audit scope provided
- Directly applicable to the identified process areas
- Focused on high-risk areas
- Actionable during the audit
- Based on current regulatory expectations
- **Very important**: Think carefully and Quote the requirement text verbatim from the citation identified for each requirement

Begin with the most critical requirements first."""
    
    return prompt

def clean_json_string(json_str):
    """Clean up common JSON formatting issues"""
    import re
    
    # Remove any BOM or special characters at start
    json_str = json_str.lstrip('\ufeff\xef\xbb\xbf')
    
    # Fix trailing commas in arrays and objects
    json_str = re.sub(r',\s*}', '}', json_str)
    json_str = re.sub(r',\s*]', ']', json_str)
    
    # Fix missing commas between array/object items
    # This is tricky - only add if needed
    
    return json_str

def fix_common_json_errors(response):
    """Attempt to fix common JSON errors in LLM responses"""
    import re
    
    # Extract JSON portion
    if "```json" in response:
        json_start = response.find("```json") + 7
        json_end = response.find("```", json_start)
        json_str = response[json_start:json_end].strip()
    elif "```" in response:
        json_start = response.find("```") + 3
        json_end = response.find("```", json_start)
        json_str = response[json_start:json_end].strip()
    else:
        # Try to find JSON object boundaries
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            json_str = json_match.group(0)
        else:
            json_str = response.strip()
    
    # Clean up
    json_str = clean_json_string(json_str)
    
    # Fix unescaped quotes in strings (common issue)
    # This is complex and risky - be careful
    
    # Fix unescaped newlines in strings
    json_str = re.sub(r'(?<!\\)\n(?=[^"]*"(?:[^"]*"[^"]*")*[^"]*$)', r'\\n', json_str)
    
    return json_str

def parse_llm_response(response):
    """Parse Claude's JSON response with robust error handling"""
    try:
        # Extract JSON from response (handle markdown code blocks if present)
        if "```json" in response:
            json_start = response.find("```json") + 7
            json_end = response.find("```", json_start)
            json_str = response[json_start:json_end].strip()
        elif "```" in response:
            json_start = response.find("```") + 3
            json_end = response.find("```", json_start)
            json_str = response[json_start:json_end].strip()
        else:
            json_str = response.strip()
        
        # Clean up common JSON issues
        json_str = clean_json_string(json_str)
        
        data = json.loads(json_str)
        
        # New flat structure - just requirements array
        requirements = data.get('requirements', [])
        
        # Group by category for frontend compatibility
        categories_dict = {}
        for req in requirements:
            category = req.get('category', 'Other')
            if category not in categories_dict:
                categories_dict[category] = {
                    'category_name': category,
                    'requirements': []
                }
            categories_dict[category]['requirements'].append(req)
        
        # Build response in expected format
        categories = list(categories_dict.values())
        for cat in categories:
            cat['requirement_count'] = len(cat['requirements'])
        
        return {
            "total_requirements": len(requirements),
            "categories": categories,
            "raw_requirements": requirements  # Keep original flat list
        }
        
    except json.JSONDecodeError as e:
        print(f"Error parsing Claude response: {e}")
        print(f"Response was: {response[:500]}...")
        
        # Try to fix common JSON errors and retry
        try:
            fixed_json = fix_common_json_errors(response)
            data = json.loads(fixed_json)
            requirements = data.get('requirements', [])
            
            # Group by category
            categories_dict = {}
            for req in requirements:
                category = req.get('category', 'Other')
                if category not in categories_dict:
                    categories_dict[category] = {
                        'category_name': category,
                        'requirements': []
                    }
                categories_dict[category]['requirements'].append(req)
            
            categories = list(categories_dict.values())
            for cat in categories:
                cat['requirement_count'] = len(cat['requirements'])
            
            return {
                "total_requirements": len(requirements),
                "categories": categories,
                "raw_requirements": requirements
            }
        except Exception as retry_error:
            print(f"Retry also failed: {retry_error}")
            
            # Return minimal structure if all parsing fails
            return {
                "total_requirements": 0,
                "categories": [],
                "error": "Failed to parse LLM response"
            }
    except Exception as e:
        print(f"Unexpected error in parse_llm_response: {e}")
        return {
            "total_requirements": 0,
            "categories": [],
            "error": f"Failed to parse LLM response: {str(e)}"
        }

# ============================================================================
# API ROUTES
# ============================================================================

@app.route('/')
def serve_frontend():
    """Serve the main HTML file"""
    return send_file('audit_poc.html')

@app.route('/api/upload', methods=['POST'])
def upload_files():
    """Handle file uploads"""
    try:
        if 'files' not in request.files:
            return jsonify({'success': False, 'message': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        uploaded_documents = []
        
        for file in files:
            if file.filename == '':
                continue
                
            if not allowed_file(file.filename):
                return jsonify({
                    'success': False, 
                    'message': f'File {file.filename} is not a supported format'
                }), 400
            
            # Generate unique filename
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            
            # Save file
            file.save(file_path)
            
            # Get file info
            file_size = get_file_size_mb(file_path)
            upload_date = datetime.now().strftime('%Y-%m-%d')
            
            # Determine document category based on filename
            filename_lower = file.filename.lower()
            if 'master' in filename_lower or 'site' in filename_lower:
                category = 'Site Master File'
            elif 'sop' in filename_lower:
                if 'gown' in filename_lower or 'asep' in filename_lower:
                    category = 'Aseptic Process SOPs'
                else:
                    category = 'Quality System SOPs'
            elif 'batch' in filename_lower or 'mbr' in filename_lower:
                category = 'Aseptic Process SOPs'
            else:
                category = 'Other Documents'
            
            # Create document record
            document = {
                'id': f'doc-{uuid.uuid4().hex[:8]}',
                'title': os.path.splitext(file.filename)[0],
                'type': file_extension.upper()[1:],
                'size': f'{file_size} MB',
                'uploadDate': upload_date,
                'status': 'Analyzing',
                'thumbnail': generate_thumbnail_path(file_path),
                'fullDocument': f'/api/document/{unique_filename}',
                'category': category,
                'filename': unique_filename
            }
            
            uploaded_documents.append(document)
        
        return jsonify({
            'success': True,
            'message': f'Successfully uploaded {len(uploaded_documents)} file(s)',
            'documents': uploaded_documents
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Upload failed: {str(e)}'
        }), 500

@app.route('/api/documents', methods=['GET'])
def get_documents():
    """Get list of all uploaded documents"""
    try:
        documents = []
        
        for filename in os.listdir(UPLOAD_FOLDER):
            if allowed_file(filename):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file_size = get_file_size_mb(file_path)
                upload_date = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d')
                
                # Determine category
                filename_lower = filename.lower()
                if 'master' in filename_lower or 'site' in filename_lower:
                    category = 'Site Master File'
                elif 'sop' in filename_lower:
                    if 'gown' in filename_lower or 'asep' in filename_lower:
                        category = 'Aseptic Process SOPs'
                    else:
                        category = 'Quality System SOPs'
                elif 'batch' in filename_lower or 'mbr' in filename_lower:
                    category = 'Aseptic Process SOPs'
                else:
                    category = 'Other Documents'
                
                document = {
                    'id': f'doc-{uuid.uuid4().hex[:8]}',
                    'title': os.path.splitext(filename)[0],
                    'type': os.path.splitext(filename)[1].upper()[1:],
                    'size': f'{file_size} MB',
                    'uploadDate': upload_date,
                    'status': 'Analyzed',
                    'thumbnail': generate_thumbnail_path(file_path),
                    'fullDocument': f'/api/document/{filename}',
                    'category': category,
                    'filename': filename
                }
                
                documents.append(document)
        
        return jsonify({'success': True, 'documents': documents})
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to retrieve documents: {str(e)}'
        }), 500

@app.route('/api/document/<filename>')
def serve_document(filename):
    """Serve uploaded documents"""
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        # For PDFs, serve directly
        if filename.lower().endswith('.pdf'):
            return send_file(file_path, as_attachment=False)
        
        # For other files, serve as attachment
        return send_file(file_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/document/<filename>/download')
def download_document(filename):
    """Download a specific document"""
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(file_path, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate-requirements', methods=['POST'])
def generate_requirements():
    """
    Generate regulatory requirements based on audit scope using Databricks Claude Sonnet 3.5
    
    Expected POST body:
    {
        "facility": "PharmaCore Site C - Aseptic Filling Suite 2",
        "process_areas": ["Grade A/B Aseptic Filling", "Environmental Monitoring"],
        "products": "Injectable biologics (mAbs)",
        "time_period": "January 2024 - December 2024",
        "key_systems": ["QMS", "Training System", "CAPA"],
        "regulatory_requirements": ["21 CFR Part 211", "EU GMP Annex 1"]
    }
    """
    try:
        audit_scope = request.json
        
        # Validate input
        if not audit_scope:
            return jsonify({'error': 'No audit scope provided'}), 400
        
        # Build prompt
        prompt = build_requirements_prompt(audit_scope)
        
        # Call Claude Sonnet 3.5
        print("Calling Databricks Claude Sonnet 4.5...")
        llm_response = call_claude(prompt)
        
        # Parse response
        requirements = parse_llm_response(llm_response)
        
        # Check if parsing failed
        if 'error' in requirements and requirements['total_requirements'] == 0:
            error_msg = f"Failed to parse LLM response. The AI returned invalid JSON. Please try again."
            print(error_msg)
            print(f"Raw LLM response: {llm_response[:1000]}...")
            return jsonify({
                'error': error_msg,
                'details': 'The AI response could not be parsed as valid JSON. This is usually temporary - please try again.',
                'total_requirements': 0,
                'categories': []
            }), 200  # Return 200 so frontend can display error message
        
        print(f"✅ Generated {requirements.get('total_requirements', 0)} requirements")
        
        return jsonify(requirements), 200
        
    except Exception as e:
        error_msg = f'Failed to generate requirements: {str(e)}'
        print(f"❌ Error: {error_msg}")
        import traceback
        print(traceback.format_exc())
        return jsonify({
            'error': error_msg,
            'details': 'An unexpected error occurred. Please check the server logs.',
            'total_requirements': 0,
            'categories': []
        }), 500

# ============================================================================
# OBSERVATION MANAGEMENT
# ============================================================================

# In-memory storage for observations (replace with database in production)
observations_db = []
observation_counter = 1

@app.route('/api/observations', methods=['GET'])
def get_observations():
    """Get all observations, optionally filtered by requirement"""
    requirement_id = request.args.get('requirement_id')
    
    if requirement_id:
        filtered = [obs for obs in observations_db if obs.get('linkedRequirement', {}).get('id') == requirement_id]
        return jsonify({'success': True, 'observations': filtered})
    
    return jsonify({'success': True, 'observations': observations_db})

@app.route('/api/observations', methods=['POST'])
def create_observation():
    """Create a new observation"""
    global observation_counter
    
    try:
        data = request.json
        
        # Handle both single linkedRequirement (legacy) and linkedRequirements (array)
        linked_requirements = data.get('linkedRequirements', [])
        if not linked_requirements and data.get('linkedRequirement'):
            linked_requirements = [data.get('linkedRequirement')]
        
        observation = {
            'id': f'OBS-{observation_counter:03d}',
            'linkedRequirement': linked_requirements[0] if linked_requirements else None,  # For backward compatibility
            'linkedRequirements': linked_requirements,  # New field for multi-select
            'observationText': data.get('observationText', ''),
            'complianceStatus': data.get('complianceStatus', 'gap'),  # compliant | gap | non-compliant
            'severity': data.get('severity', 'medium'),  # critical | major | minor
            'category': data.get('category', ''),
            'evidence': data.get('evidence', []),
            'metadata': {
                'location': data.get('location', ''),
                'auditor': data.get('auditor', 'Current User'),
                'interviewed': data.get('interviewed', ''),
                'imageDescription': data.get('imageDescription', ''),
                'audioTranscription': data.get('audioTranscription', ''),
                'handwrittenTranscription': data.get('handwrittenTranscription', ''),
                'timestamp': datetime.now().isoformat(),
                'lastUpdated': datetime.now().isoformat()
            },
            'aiAnalysis': data.get('aiAnalysis', {}),
            'followUp': data.get('followUp', []),
            'tags': data.get('tags', [])
        }
        
        observations_db.append(observation)
        observation_counter += 1
        
        return jsonify({
            'success': True,
            'observation': observation,
            'message': 'Observation created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to create observation: {str(e)}'
        }), 500

@app.route('/api/observations/<observation_id>', methods=['GET'])
def get_observation(observation_id):
    """Get a specific observation"""
    observation = next((obs for obs in observations_db if obs['id'] == observation_id), None)
    
    if observation:
        return jsonify({'success': True, 'observation': observation})
    else:
        return jsonify({'success': False, 'error': 'Observation not found'}), 404

@app.route('/api/observations/<observation_id>', methods=['PUT'])
def update_observation(observation_id):
    """Update an existing observation"""
    try:
        observation = next((obs for obs in observations_db if obs['id'] == observation_id), None)
        
        if not observation:
            return jsonify({'success': False, 'error': 'Observation not found'}), 404
        
        data = request.json
        
        # Update fields
        observation['observationText'] = data.get('observationText', observation['observationText'])
        observation['complianceStatus'] = data.get('complianceStatus', observation['complianceStatus'])
        observation['severity'] = data.get('severity', observation['severity'])
        observation['evidence'] = data.get('evidence', observation['evidence'])
        observation['followUp'] = data.get('followUp', observation['followUp'])
        observation['metadata']['lastUpdated'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'observation': observation,
            'message': 'Observation updated successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to update observation: {str(e)}'
        }), 500

@app.route('/api/observations/<observation_id>', methods=['DELETE'])
def delete_observation(observation_id):
    """Delete an observation"""
    global observations_db
    
    observation = next((obs for obs in observations_db if obs['id'] == observation_id), None)
    
    if observation:
        observations_db = [obs for obs in observations_db if obs['id'] != observation_id]
        return jsonify({'success': True, 'message': 'Observation deleted successfully'})
    else:
        return jsonify({'success': False, 'error': 'Observation not found'}), 404

@app.route('/api/observations/stats', methods=['GET'])
def get_observation_stats():
    """Get observation statistics"""
    stats = {
        'total': len(observations_db),
        'by_status': {
            'compliant': len([o for o in observations_db if o['complianceStatus'] == 'compliant']),
            'gap': len([o for o in observations_db if o['complianceStatus'] == 'gap']),
            'non_compliant': len([o for o in observations_db if o['complianceStatus'] == 'non-compliant'])
        },
        'by_severity': {
            'critical': len([o for o in observations_db if o['severity'] == 'critical']),
            'major': len([o for o in observations_db if o['severity'] == 'major']),
            'minor': len([o for o in observations_db if o['severity'] == 'minor'])
        },
        'total_evidence': sum(len(o.get('evidence', [])) for o in observations_db)
    }
    
    return jsonify({'success': True, 'stats': stats})

@app.route('/api/audio/transcribe', methods=['POST'])
def transcribe_audio():
    """
    Transcribe audio file using Whisper model with Databricks dataframe_split format
    Expects: multipart/form-data with 'audio' file
    Returns: transcribed text
    """
    try:
        if not WHISPER_HOST or not DATABRICKS_TOKEN:
            return jsonify({
                'success': False,
                'error': 'Whisper service not configured. Please set WHISPER_HOST and DATABRICKS_TOKEN in environment variables.'
            }), 503
        
        # Check if audio file is in request
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        
        if audio_file.filename == '':
            return jsonify({'success': False, 'error': 'No audio file selected'}), 400
        
        # Save audio file temporarily
        audio_filename = f"temp_{uuid.uuid4()}.webm"
        audio_path = os.path.join(app.config['AUDIO_FOLDER'], audio_filename)
        audio_file.save(audio_path)
        
        print(f"Transcribing audio: {audio_filename}")
        
        try:
            # Read and encode the audio file to base64
            with open(audio_path, "rb") as f:
                audio_base64 = base64.b64encode(f.read()).decode("utf-8")
            
            # Define the JSON payload in dataframe_split format
            # Use positional indexing (0) instead of column names
            payload = {
                "dataframe_split": {
                    "columns": [0],
                    "data": [[audio_base64]]
                }
            }
            
            # Set the authentication header
            headers = {
                "Authorization": f"Bearer {DATABRICKS_TOKEN}",
                "Content-Type": "application/json"
            }
            
            # Send the POST request to the Databricks endpoint
            print(f"Sending request to Whisper endpoint: {WHISPER_HOST}")
            response = requests.post(WHISPER_HOST, headers=headers, json=payload, timeout=120)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            # Clean up temp file
            os.remove(audio_path)
            
            # Parse and extract the transcription
            result = response.json()
            transcription = result.get("predictions", [None])[0]
            
            if not transcription:
                raise ValueError("No transcription returned from Whisper API")
            
            print(f"Transcription successful: {len(transcription)} characters")
            
            return jsonify({
                'success': True,
                'transcription': transcription
            })
            
        except requests.exceptions.HTTPError as e:
            # Clean up temp file on error
            if os.path.exists(audio_path):
                os.remove(audio_path)
            error_msg = f'HTTP error from Whisper API: {e.response.status_code} - {e.response.text}'
            print(error_msg)
            raise Exception(error_msg)
            
        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(audio_path):
                os.remove(audio_path)
            raise e
            
    except Exception as e:
        error_msg = f'Failed to transcribe audio: {str(e)}'
        print(error_msg)
        import traceback
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': error_msg}), 500

@app.route('/api/handwritten/transcribe', methods=['POST'])
def transcribe_handwritten():
    """
    Transcribe handwritten notes using Claude Vision API
    Expects: Base64 encoded image
    Returns: Transcribed text
    """
    try:
        if not DATABRICKS_HOST or not DATABRICKS_TOKEN:
            return jsonify({
                'success': False,
                'error': 'LLM service not configured. Please set DATABRICKS_HOST and DATABRICKS_TOKEN.'
            }), 503
        
        data = request.json
        image_base64 = data.get('image', '')
        
        if not image_base64:
            return jsonify({'success': False, 'error': 'No image provided'}), 400
        
        # Prepare prompt for OCR
        prompt = """Please transcribe all handwritten text from this image. 

Instructions:
- Extract all handwritten text exactly as written
- Maintain the structure and organization of the notes
- Include any diagrams or sketches descriptions in [brackets]
- If text is unclear or illegible, indicate with [illegible]
- Preserve bullet points, numbering, and formatting
- Include any signatures, dates, or timestamps

Provide only the transcribed text, without any additional commentary or explanations."""

        # Call Claude Vision API
        response_text = call_claude_with_vision(prompt, image_base64, max_tokens=2000)
        
        return jsonify({
            'success': True,
            'transcription': response_text
        })
        
    except Exception as e:
        error_msg = f'Failed to transcribe handwritten notes: {str(e)}'
        print(error_msg)
        import traceback
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': error_msg}), 500

@app.route('/api/observations/analyze', methods=['POST'])
def analyze_observation():
    """
    AI-powered analysis of observation to auto-tag requirement and extract insights
    Accepts: text observation + optional images (up to 5 base64) + optional audio transcription
    Returns: Suggested requirement match, citations, compliance status, severity
    """
    try:
        data = request.json
        
        observation_text = data.get('observationText', '')
        image_description = data.get('imageDescription', '')  # Manual description (optional)
        image_data = data.get('imageData', [])  # Can be array of Base64 images or single image
        audio_transcription = data.get('audioTranscription', '')  # From speech-to-text
        available_requirements = data.get('requirements', [])  # List of generated requirements
        
        # Normalize image_data to always be a list
        if isinstance(image_data, str) and image_data:
            image_data = [image_data]
        elif not isinstance(image_data, list):
            image_data = []
        
        # Filter out empty strings
        image_data = [img for img in image_data if img]
        
        if not observation_text and not image_description and not audio_transcription and not image_data:
            return jsonify({
                'success': False,
                'error': 'At least one input (text, image, or audio) is required'
            }), 400
        
        num_images = len(image_data)
        print(f"Analyzing observation with Claude...")
        print(f"Text: {len(observation_text)} chars, Images: {num_images}, Audio: {len(audio_transcription)} chars")
        
        # Build comprehensive prompt for Claude
        prompt = build_observation_analysis_prompt(
            observation_text, 
            image_description, 
            audio_transcription,
            available_requirements,
            num_images=num_images
        )
        
        # Call Claude - with vision if images provided
        if image_data:
            print(f"Using Claude VISION API for {num_images} image(s) analysis")
            llm_response = call_claude_with_multiple_images(prompt, image_data, max_tokens=4000)
        else:
            llm_response = call_claude(prompt, max_tokens=2000)
        
        print(f"Claude response received")
        
        # Parse response
        analysis = parse_observation_analysis(llm_response)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        error_msg = f'Failed to analyze observation: {str(e)}'
        print(error_msg)
        import traceback
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': error_msg}), 500

def build_observation_analysis_prompt(observation_text, image_desc, audio_trans, requirements, num_images=0):
    """Build prompt for AI observation analysis"""
    
    # Combine all inputs
    combined_observation = ""
    
    if observation_text:
        combined_observation += f"WRITTEN OBSERVATION:\n{observation_text}\n\n"
    
    if num_images > 0:
        image_word = "images" if num_images > 1 else "image"
        combined_observation += f"VISUAL EVIDENCE:\n{num_images} {image_word} {'have' if num_images > 1 else 'has'} been provided. Please analyze the visual content across all images to identify any GxP compliance issues, non-conformities, or good practices.\n\n"
        if num_images > 1:
            combined_observation += f"⚠️ IMPORTANT: Review ALL {num_images} images carefully. They may show different angles, time points, or aspects of the same observation.\n\n"
        if image_desc:
            combined_observation += f"Auditor's Image Notes: {image_desc}\n\n"
    elif image_desc:
        combined_observation += f"IMAGE DESCRIPTION (No actual images):\n{image_desc}\n\n"
    
    if audio_trans:
        combined_observation += f"AUDIO NOTES:\n{audio_trans}\n\n"
    
    # Build requirements context
    req_context = "AVAILABLE REQUIREMENTS:\n"
    for req in requirements:
        req_text = req.get('requirement_text (verbatim)') or req.get('requirement_text', '')
        citation = req.get('citation', 'N/A')
        
        req_context += f"\n{req['id']}:\n"
        req_context += f"  Citation: {citation}\n"
        req_context += f"  Category: {req.get('category', 'N/A')}\n"
        req_context += f"  Risk Level: {req.get('risk_level', 'N/A')}\n"
        req_context += f"  Requirement: {req_text[:200]}...\n"
    
    vision_instructions = ""
    if num_images > 0:
        image_plural = "IMAGES" if num_images > 1 else "IMAGE"
        vision_instructions = f"""
⚠️ VISUAL EVIDENCE PROVIDED - Analyze {"all" if num_images > 1 else "the"} {num_images} {image_plural.lower()} carefully!

{f"IMPORTANT: You have been provided {num_images} images. Review EACH image thoroughly and consider them together as a comprehensive view of the observation." if num_images > 1 else ""}

When analyzing the {"images" if num_images > 1 else "image"}, look for:
- Personnel practices (gowning, aseptic technique, hand hygiene)
- Equipment condition and maintenance
- Documentation (completeness, accuracy, signatures, dates)
- Environmental conditions (cleanliness, organization, contamination risks)
- Process compliance (procedures being followed, deviations)
- Product handling and storage
- Safety hazards or patient safety risks

{"For multiple images: Note if they show the same issue from different angles, a sequence of events, or multiple separate issues." if num_images > 1 else ""}

Describe what you observe in the {"images" if num_images > 1 else "image"} and connect to regulatory requirements.
"""
    
    prompt = f"""You are a GxP regulatory compliance expert analyzing an audit observation. Your task is to:

1. {f"ANALYZE THE PROVIDED {num_images} {'IMAGES' if num_images > 1 else 'IMAGE'} for compliance issues" if num_images > 0 else "Review the observation details"}
2. Identify which requirement(s) this observation relates to
3. Determine the compliance status
4. Assess the severity
5. Suggest relevant citations
6. Provide analysis and recommendations

{vision_instructions}

OBSERVATION TO ANALYZE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{combined_observation}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{req_context}

ANALYSIS INSTRUCTIONS:
1. Match this observation to the MOST relevant requirement(s) from the list above
2. Determine if this represents:
   - COMPLIANT: No issues, good practice observed
   - GAP: Minor deviation or opportunity for improvement
   - NON_COMPLIANT: Significant regulatory violation

3. Assess severity (if gap/non-compliant):
   - CRITICAL: Immediate patient safety risk or major GMP violation
   - MAJOR: Significant compliance issue requiring CAPA
   - MINOR: Opportunity for improvement

4. Identify any additional regulatory citations mentioned or implied
5. Provide brief analysis and recommendations

Respond ONLY with valid JSON in this exact format:
{{
  "matched_requirements": [
    {{
      "requirement_id": "req_001",
      "confidence": 0.95,
      "reasoning": "This observation directly relates to EM investigation timeliness"
    }}
  ],
  "compliance_status": "gap",
  "severity": "major",
  "additional_citations": [
    "21 CFR 211.22",
    "EU GMP Chapter 1"
  ],
  "analysis": "The observation indicates that investigation EX-24-0312 was not completed within the required timeframe specified in EU GMP Annex 1 § 4.29. This represents a gap in the QMS procedure execution.",
  "recommendations": [
    "Initiate CAPA to address investigation timeliness",
    "Review SOP-EM-001 for clarity on investigation timelines",
    "Provide additional training to EM team on investigation procedures"
  ],
  "key_findings": [
    "Investigation completed 5 days late",
    "No CAPA initiated for the delay",
    "Potential systemic issue with investigation turnaround"
  ],
  "evidence_needed": [
    "Investigation report EX-24-0312",
    "SOP-EM-001 (investigation procedure)",
    "Training records for EM coordinator",
    "Trending data for investigation timeliness"
  ],{("" if num_images == 0 else "")}
  {('"visual_findings": "Describe what you see across all images that relates to compliance. If multiple images, reference each one (e.g., \'Image 1 shows..., Image 2 shows...\')",' if num_images > 0 else "")}
  "suggested_observation_text": "Write a professional, detailed observation statement that incorporates all evidence provided (written notes, images, audio). Use factual language and include specific details like dates, times, locations, people interviewed, document numbers, and what was observed. Structure it as: 'During [activity], at [location], on [date/time], I observed [specific finding]. [Additional context]. This was documented in [reference].' Make it comprehensive and audit-ready."
}}

{(f"For the visual_findings field, describe specific details you observe across all {num_images} images that support your analysis. Reference individual images when relevant." if num_images > 1 else "For the visual_findings field, describe specific details you observe in the image that support your analysis." if num_images == 1 else "")}

For the suggested_observation_text field, synthesize ALL evidence into one professional observation statement. Include location, people interviewed, specific findings, document references, and timestamps when available.

Think carefully about the regulatory context and implications. Be specific and actionable."""
    
    return prompt

def parse_observation_analysis(response):
    """Parse Claude's observation analysis response"""
    try:
        # Extract JSON from response
        if "```json" in response:
            json_start = response.find("```json") + 7
            json_end = response.find("```", json_start)
            json_str = response[json_start:json_end].strip()
        elif "```" in response:
            json_start = response.find("```") + 3
            json_end = response.find("```", json_start)
            json_str = response[json_start:json_end].strip()
        else:
            json_str = response.strip()
        
        analysis = json.loads(json_str)
        return analysis
        
    except json.JSONDecodeError as e:
        print(f"Error parsing analysis response: {e}")
        print(f"Response was: {response[:500]}...")
        
        return {
            "matched_requirements": [],
            "compliance_status": "gap",
            "severity": "medium",
            "additional_citations": [],
            "analysis": "Unable to parse AI response",
            "recommendations": [],
            "key_findings": [],
            "evidence_needed": [],
            "error": "Failed to parse AI response"
        }

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy', 
        'message': 'Audit POC API is running',
        'llm_configured': bool(DATABRICKS_TOKEN and DATABRICKS_TOKEN != 'your-token')
    })

if __name__ == '__main__':
    print("Starting Audit POC Flask Server...")
    print("Frontend available at: http://localhost:5000")
    print("API endpoints available at: http://localhost:5000/api/")
    app.run(debug=True, host='0.0.0.0', port=5000)
