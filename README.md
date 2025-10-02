# Audit POC - Document Upload System

A comprehensive audit management system with document upload capabilities, built with HTML/CSS/JavaScript frontend and Python Flask backend.

## Features

### Frontend (HTML/CSS/JavaScript)
- **Pre-Audit Prep Tab**: Document request status and AI-generated focus areas
- **Document Upload**: Drag-and-drop file upload with progress indicators
- **Document Gallery**: Visual display of uploaded documents with thumbnails
- **Document Viewer**: Full-screen modal viewer for document inspection
- **Live Fieldwork Tab**: Audit agenda and evidence capture
- **Finalization Tab**: Findings summary and report generation

### Backend (Python Flask)
- **File Upload API**: Handle multiple file uploads with validation
- **Document Serving**: Serve uploaded documents and thumbnails
- **File Management**: Secure file storage and retrieval
- **Integrated Frontend**: Serves HTML frontend from same server

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project files**
   ```bash
   # Ensure you have these files in your project directory:
   # - audit_poc.html
   # - app.py
   # - requirements.txt
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create upload directory**
   ```bash
   mkdir uploads
   ```

4. **Run the Flask server**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your web browser
   - Navigate to: `http://localhost:5000`
   - The audit POC interface will load automatically

## API Endpoints

### Document Management
- `POST /api/upload` - Upload multiple documents
- `GET /api/documents` - Get list of all uploaded documents
- `GET /api/document/<filename>` - Serve/view a specific document
- `GET /api/document/<filename>/download` - Download a specific document

### Audio Transcription
- `POST /api/transcribe` - Transcribe audio to text (server-side processing)
  - Accepts: audio file (webm, wav, mp3, ogg, m4a)
  - Returns: JSON with transcription text
  - **Note**: Currently returns placeholder transcription. Integrate with speech-to-text service for production.

### System
- `GET /api/health` - Health check endpoint
- `GET /` - Serve the main frontend application

## File Upload Features

### Supported File Types
- **Documents**: PDF (.pdf), Microsoft Word (.doc, .docx)
- **Audio**: WebM, WAV, MP3, OGG, M4A

### File Validation
- Maximum document size: 10MB per file
- Maximum audio size: 50MB per file
- File type validation
- Secure filename handling

### Upload Process
1. **Drag & Drop**: Drag files onto the upload area
2. **Click to Select**: Click the upload area to open file browser
3. **Progress Tracking**: Real-time upload progress indicator
4. **Status Feedback**: Success/error messages with auto-hide
5. **Gallery Update**: New documents automatically appear in gallery

## Document Categories

Documents are automatically categorized based on filename:
- **Site Master File**: Files containing "master" or "site"
- **Quality System SOPs**: Files containing "sop" (except aseptic)
- **Aseptic Process SOPs**: Files containing "gown", "asep", or "batch"
- **Other Documents**: All other uploaded files

## Voice Transcription

The application includes voice-to-text functionality for observation descriptions:

### Current Implementation
- **Client-side**: Records audio using browser MediaRecorder API
- **Server-side**: Processes audio via `/api/transcribe` endpoint
- **Placeholder**: Returns simulated transcription based on audio length

### Production Integration

To enable real transcription, integrate a speech-to-text service in `app.py`:

#### Option 1: OpenAI Whisper API
```python
import openai

def transcribe_audio_placeholder(audio_path):
    with open(audio_path, 'rb') as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript['text']
```

#### Option 2: Local Whisper Model
```bash
pip install openai-whisper
```
```python
import whisper

model = whisper.load_model("base")

def transcribe_audio_placeholder(audio_path):
    result = model.transcribe(audio_path)
    return result["text"]
```

#### Option 3: Google Cloud Speech-to-Text
```bash
pip install google-cloud-speech
```

#### Option 4: Azure Speech Services
```bash
pip install azure-cognitiveservices-speech
```

## Development

### Project Structure
```
audit-poc/
├── audit_poc.html      # Frontend application
├── app.py              # Flask backend server
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── uploads/           # Uploaded files directory (created automatically)
```

### Customization

#### Adding New File Types
1. Update `ALLOWED_EXTENSIONS` in `app.py`
2. Update `validTypes` array in `audit_poc.html`
3. Add appropriate MIME type handling

#### Modifying Upload Limits
1. Update `MAX_FILE_SIZE` in `app.py`
2. Update `maxSize` variable in `audit_poc.html`

#### Styling Changes
- Modify CSS classes in `audit_poc.html`
- Update Tailwind CSS classes for different appearance

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   - Change port in `app.py`: `app.run(port=5001)`
   - Update frontend API calls to use new port

2. **File Upload Fails**
   - Check file size (must be < 10MB)
   - Verify file type is supported
   - Ensure uploads directory exists and is writable

3. **Frontend Not Loading**
   - Ensure audit_poc.html is in the same directory as app.py
   - Check that Flask server is running on correct port

4. **Documents Not Displaying**
   - Verify files are in the uploads directory
   - Check browser console for JavaScript errors
   - Ensure API endpoints are responding correctly

### Logs
- Flask server logs are displayed in the terminal
- Check browser developer console for frontend errors
- API responses include error messages for debugging

## Security Notes

- Files are stored with UUID-based names to prevent conflicts
- File type validation prevents malicious uploads
- File size limits prevent resource exhaustion
- Frontend and backend served from same origin (no CORS needed)

## Production Deployment

For production deployment:
1. Use a production WSGI server (e.g., Gunicorn)
2. Implement user authentication
3. Add file encryption for sensitive documents
4. Use a proper database for document metadata
5. Implement backup and recovery procedures
6. Configure proper static file serving
