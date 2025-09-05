from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import elevenlabs
import os
import tempfile
import uuid
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# API Keys (Replace with your actual keys or use environment variables)
ELEVENLABS_API_KEY = os.environ["ELEVENLABS_API_KEY"]

# Available voices for ElevenLabs
AVAILABLE_VOICES = {
    "rachel": "21m00Tcm4TlvDq8ikWAM",      # Female voice
    "domi": "AZnzlk1XvdvUeBnXmlld",        # Female voice
    "bella": "EXAVITQu4vr4xnSDxMaL",       # Female voice
    "antoni": "ErXwobaYiN1P8YkM0tQj",      # Male voice
    "thomas": "GBv7mTt0atIp3Br8iCZE",      # Male voice
    "josh": "TxGEqnHWrfWFTfGW9XjX",        # Male voice
    "arnold": "VR6AewLTigWG4xSOukaG",      # Male voice
    "adam": "pNInz6obpgDQGcFmaJgB",        # Male voice
    "sam": "yoZ06aMxZJJ28mfd3POQ",         # Male voice
    "default": "21m00Tcm4TlvDq8ikWAM"     # Default voice
}

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "AI Movie Dialogue Audio Generator API"
    })

@app.route('/voices', methods=['GET'])
def get_available_voices():
    """Get list of available voices"""
    return jsonify({
        "voices": AVAILABLE_VOICES,
        "message": "Available voices for audio generation"
    })

@app.route('/generate-dialogue-audio', methods=['POST'])
def generate_dialogue_audio():
    """
    Generate dialogue audio from text using ElevenLabs API
    
    Expected JSON payload:
    {
        "text": "The dialogue text to convert to speech",
        "voice_id": "voice_id_or_name" (optional, defaults to "default"),
        "output_format": "mp3" (optional, defaults to "mp3")
    }
    
    Returns:
    - Audio file as attachment
    - JSON response with metadata
    """
    try:
        # Validate request
        if not request.is_json:
            return jsonify({
                "error": "Content-Type must be application/json"
            }), 400
        
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                "error": "Missing required field: 'text'"
            }), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({
                "error": "Text cannot be empty"
            }), 400
        
        # Get voice ID
        voice_input = data.get('voice_id', 'default')
        voice_id = AVAILABLE_VOICES.get(voice_input.lower(), voice_input)
        
        # Get output format
        output_format = data.get('output_format', 'mp3')
        
        logger.info(f"Generating audio for text: {text[:50]}... with voice: {voice_id}")
        
        # Initialize ElevenLabs client
        client = elevenlabs.ElevenLabs(api_key=ELEVENLABS_API_KEY)
        
        # Generate audio
        audio_data = client.generate(
            text=text,
            voice=voice_id,
            model="eleven_monolingual_v1"
        )
        
        # Create temporary file
        temp_dir = tempfile.gettempdir()
        filename = f"dialogue_{uuid.uuid4().hex[:8]}.{output_format}"
        file_path = os.path.join(temp_dir, filename)
        
        with open(file_path, "wb") as f:
            f.write(audio_data)
        
        logger.info(f"Audio generated successfully: {file_path}")
        
        # Return audio file and metadata
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype=f'audio/{output_format}'
        )
        
    except Exception as e:
        logger.error(f"Error generating dialogue audio: {str(e)}")
        return jsonify({
            "error": "Failed to generate dialogue audio",
            "details": str(e)
        }), 500

@app.route('/generate-dialogue-audio-stream', methods=['POST'])
def generate_dialogue_audio_stream():
    """
    Generate dialogue audio and return as streaming response
    
    Expected JSON payload:
    {
        "text": "The dialogue text to convert to speech",
        "voice_id": "voice_id_or_name" (optional, defaults to "default")
    }
    
    Returns:
    - Audio data as streaming response
    """
    try:
        # Validate request
        if not request.is_json:
            return jsonify({
                "error": "Content-Type must be application/json"
            }), 400
        
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                "error": "Missing required field: 'text'"
            }), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({
                "error": "Text cannot be empty"
            }), 400
        
        # Get voice ID
        voice_input = data.get('voice_id', 'default')
        voice_id = AVAILABLE_VOICES.get(voice_input.lower(), voice_input)
        
        logger.info(f"Generating streaming audio for text: {text[:50]}... with voice: {voice_id}")
        
        # Initialize ElevenLabs client
        client = elevenlabs.ElevenLabs(api_key=ELEVENLABS_API_KEY)
        
        # Generate audio
        audio_data = client.generate(
            text=text,
            voice=voice_id,
            model="eleven_monolingual_v1"
        )
        
        logger.info("Audio generated successfully for streaming")
        
        # Return audio data as streaming response
        return app.response_class(
            audio_data,
            status=200,
            mimetype='audio/mpeg'
        )
        
    except Exception as e:
        logger.error(f"Error generating streaming dialogue audio: {str(e)}")
        return jsonify({
            "error": "Failed to generate dialogue audio",
            "details": str(e)
        }), 500

@app.route('/generate-dialogue-audio-info', methods=['POST'])
def generate_dialogue_audio_info():
    """
    Generate dialogue audio and return metadata without the actual audio file
    
    Expected JSON payload:
    {
        "text": "The dialogue text to convert to speech",
        "voice_id": "voice_id_or_name" (optional, defaults to "default")
    }
    
    Returns:
    - JSON response with audio metadata and base64 encoded audio
    """
    try:
        # Validate request
        if not request.is_json:
            return jsonify({
                "error": "Content-Type must be application/json"
            }), 400
        
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                "error": "Missing required field: 'text'"
            }), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({
                "error": "Text cannot be empty"
            }), 400
        
        # Get voice ID
        voice_input = data.get('voice_id', 'default')
        voice_id = AVAILABLE_VOICES.get(voice_input.lower(), voice_input)
        
        logger.info(f"Generating audio info for text: {text[:50]}... with voice: {voice_id}")
        
        # Initialize ElevenLabs client
        client = elevenlabs.ElevenLabs(api_key=ELEVENLABS_API_KEY)
        
        # Generate audio
        audio_data = client.generate(
            text=text,
            voice=voice_id,
            model="eleven_monolingual_v1"
        )
        
        # Calculate audio duration (approximate)
        # MP3 files are typically ~128kbps, so we can estimate duration
        audio_size_bytes = len(audio_data)
        estimated_duration_seconds = (audio_size_bytes * 8) / (128 * 1000)  # Rough estimate
        
        logger.info("Audio generated successfully for info endpoint")
        
        # Return metadata
        return jsonify({
            "success": True,
            "text": text,
            "voice_id": voice_id,
            "audio_size_bytes": audio_size_bytes,
            "estimated_duration_seconds": round(estimated_duration_seconds, 2),
            "format": "mp3",
            "timestamp": datetime.now().isoformat(),
            "message": "Audio generated successfully. Use the /generate-dialogue-audio endpoint to download the actual audio file."
        })
        
    except Exception as e:
        logger.error(f"Error generating dialogue audio info: {str(e)}")
        return jsonify({
            "error": "Failed to generate dialogue audio info",
            "details": str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": [
            "GET /health",
            "GET /voices", 
            "POST /generate-dialogue-audio",
            "POST /generate-dialogue-audio-stream",
            "POST /generate-dialogue-audio-info"
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "message": "Something went wrong on our end"
    }), 500

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    print(f"🎬 AI Movie Dialogue Audio Generator API starting on port {port}")
    print(f"📖 Available endpoints:")
    print(f"   GET  /health - Health check")
    print(f"   GET  /voices - List available voices")
    print(f"   POST /generate-dialogue-audio - Generate and download audio file")
    print(f"   POST /generate-dialogue-audio-stream - Stream audio data")
    print(f"   POST /generate-dialogue-audio-info - Get audio metadata")
    print(f"\n🚀 Server starting...")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )
