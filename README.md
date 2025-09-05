# AI Movie Dialogue Audio Generator - Integrated REST API

A Flask-based REST API integrated into the main AI Movie Generation pipeline that generates dialogue audio from text using ElevenLabs' text-to-speech service. This integrated solution provides both the original movie generation pipeline and a comprehensive REST API for dialogue audio generation.

## 🚀 Features

- **Text-to-Speech Conversion**: Convert any text to natural-sounding speech
- **Multiple Voice Options**: Choose from various pre-configured voices (male/female)
- **Flexible Output Formats**: Support for different audio formats
- **Streaming Support**: Get audio data directly in the response
- **Metadata Endpoint**: Get audio information without downloading the file
- **Error Handling**: Comprehensive error handling and validation
- **CORS Support**: Cross-origin resource sharing enabled
- **Integrated Solution**: Both movie generation pipeline and REST API in one file

## 📋 Prerequisites

- Python 3.7+
- ElevenLabs API key
- Flask and other dependencies (see requirements.txt)

## 🛠️ Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**:
   - Get your ElevenLabs API key from [ElevenLabs](https://elevenlabs.io/)
   - Update the `ELEVENLABS_API_KEY` variable in `main.py`

## 🚀 Quick Start

### Option 1: Run the Movie Generation Pipeline
```bash
python main.py
```

### Option 2: Start the REST API Server
```bash
python main.py --api
```

### Option 3: Test the API
```bash
python test_api.py
```

## 📚 API Endpoints

### 1. Health Check
**GET** `/health`

Check if the API is running and healthy.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "service": "AI Movie Dialogue Audio Generator API"
}
```

### 2. Get Available Voices
**GET** `/voices`

Get a list of all available voices for audio generation.

**Response:**
```json
{
  "voices": {
    "rachel": "21m00Tcm4TlvDq8ikWAM",
    "domi": "AZnzlk1XvdvUeBnXmlld",
    "bella": "EXAVITQu4vr4xnSDxMaL",
    "antoni": "ErXwobaYiN1P8YkM0tQj",
    "thomas": "GBv7mTt0atIp3Br8iCZE",
    "josh": "TxGEqnHWrfWFTfGW9XjX",
    "arnold": "VR6AewLTigWG4xSOukaG",
    "adam": "pNInz6obpgDQGcFmaJgB",
    "sam": "yoZ06aMxZJJ28mfd3POQ",
    "default": "21m00Tcm4TlvDq8ikWAM"
  },
  "message": "Available voices for audio generation"
}
```

### 3. Generate Dialogue Audio (Download)
**POST** `/generate-dialogue-audio`

Generate audio from text and return it as a downloadable file.

**Request Body:**
```json
{
  "text": "Hello, this is a test of the dialogue audio generation API.",
  "voice_id": "rachel",
  "output_format": "mp3"
}
```

**Parameters:**
- `text` (required): The text to convert to speech
- `voice_id` (optional): Voice ID or name (defaults to "default")
- `output_format` (optional): Audio format (defaults to "mp3")

**Response:** Audio file as attachment

### 4. Generate Dialogue Audio (Stream)
**POST** `/generate-dialogue-audio-stream`

Generate audio from text and return it as a streaming response.

**Request Body:**
```json
{
  "text": "This is a streaming test of the dialogue audio generation.",
  "voice_id": "antoni"
}
```

**Response:** Audio data directly in the response body

### 5. Generate Dialogue Audio Info
**POST** `/generate-dialogue-audio-info`

Generate audio from text and return metadata without the actual audio file.

**Request Body:**
```json
{
  "text": "This is a test for getting audio metadata.",
  "voice_id": "bella"
}
```

**Response:**
```json
{
  "success": true,
  "text": "This is a test for getting audio metadata.",
  "voice_id": "EXAVITQu4vr4xnSDxMaL",
  "audio_size_bytes": 12345,
  "estimated_duration_seconds": 2.5,
  "format": "mp3",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "message": "Audio generated successfully. Use the /generate-dialogue-audio endpoint to download the actual audio file."
}
```

## 🎯 Usage Examples

### cURL Examples

**Generate and download audio:**
```bash
curl -X POST http://localhost:5000/generate-dialogue-audio \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world!", "voice_id": "rachel"}' \
  --output dialogue.mp3
```

**Get audio metadata:**
```bash
curl -X POST http://localhost:5000/generate-dialogue-audio-info \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world!", "voice_id": "antoni"}'
```

**Stream audio:**
```bash
curl -X POST http://localhost:5000/generate-dialogue-audio-stream \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world!", "voice_id": "bella"}' \
  --output stream_audio.mp3
```

### Python Examples

**Using requests library:**
```python
import requests

# Generate and download audio
response = requests.post(
    "http://localhost:5000/generate-dialogue-audio",
    json={
        "text": "Hello, this is a test!",
        "voice_id": "rachel"
    }
)

if response.status_code == 200:
    with open("output.mp3", "wb") as f:
        f.write(response.content)
    print("Audio saved successfully!")
```

**Using JavaScript/Fetch:**
```javascript
// Generate audio info
fetch('http://localhost:5000/generate-dialogue-audio-info', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        text: "Hello from JavaScript!",
        voice_id: "antoni"
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

## 🔧 Configuration

### Environment Variables

- `PORT`: Server port (default: 5000)
- `ELEVENLABS_API_KEY`: Your ElevenLabs API key

### Voice Configuration

The API includes pre-configured voices. You can modify the `AVAILABLE_VOICES` dictionary in `main.py` to add or remove voices:

```python
AVAILABLE_VOICES = {
    "rachel": "21m00Tcm4TlvDq8ikWAM",      # Female voice
    "domi": "AZnzlk1XvdvUeBnXmlld",        # Female voice
    "bella": "EXAVITQu4vr4xnSDxMaL",       # Female voice
    "antoni": "ErXwobaYiN1P8YkM0tQj",      # Male voice
    "thomas": "GBv7mTt0atIp3Br8iCZE",      # Male voice
    # Add more voices as needed
}
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_api.py
```

This will automatically start the API server, run all tests, and then stop the server.

## 📁 File Structure

```
├── main.py              # Integrated Flask API + Movie Generation Pipeline
├── test_api.py          # Test suite for the API
├── requirements.txt     # Python dependencies
└── README.md           # This documentation
```

## 🚨 Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid input (missing text, empty text, etc.)
- **404 Not Found**: Invalid endpoint
- **500 Internal Server Error**: Server-side errors

All error responses include descriptive messages and details.

## 🔒 Security Considerations

- **API Key Protection**: Store API keys in environment variables for production
- **Input Validation**: All inputs are validated and sanitized
- **Rate Limiting**: Consider implementing rate limiting for production use
- **HTTPS**: Use HTTPS in production environments

## 🚀 Production Deployment

For production deployment:

1. **Use a production WSGI server** (Gunicorn, uWSGI)
2. **Set environment variables** for configuration
3. **Implement proper logging** and monitoring
4. **Add authentication** if needed
5. **Use HTTPS** with proper SSL certificates
6. **Implement rate limiting** and request validation

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "main:app"
```

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the API.

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues:

1. Check the error logs in the console
2. Verify your API key is correct
3. Ensure all dependencies are installed
4. Check that the ElevenLabs service is accessible

For additional help, please open an issue in the project repository.
