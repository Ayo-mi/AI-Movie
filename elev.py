import re
import os
from pathlib import Path

# ElevenLabs TTS
import requests

# Your ElevenLabs API Key
ELEVENLABS_API_KEY = os.environ["ELEVENLABS_API_KEY"]

# Voice mapping: character name to ElevenLabs voice ID
CHARACTER_VOICES = {
    "RILEY": "21m00Tcm4TlvDq8ikWAM",  # Example: Rachel
    "JAMIE": "29vD33N1CtxCmqQRPOHJ"# Add more characters here
}

def parse_dialogue(script_text):
    """Extracts character lines from script markdown."""
    pattern = re.compile(r"\*\*(.+?)\*\*:\s*“(.+?)”")
    lines = pattern.findall(script_text)
    return lines  # List of tuples: (character, line)

def generate_voice(text, output_filename, voice_id):
    """Sends line to ElevenLabs and saves output to mp3."""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        with open(output_filename, "wb") as f:
            f.write(response.content)
        print(f"[✓] Audio saved: {output_filename}")
    else:
        print("[!] Error:", response.status_code, response.text)

def process_script(script_path, output_dir):
    print("""Main parser + audio generator.""")
    with open(script_path, "r", encoding="utf-8") as f:
        script_text = f.read()

    os.makedirs(output_dir, exist_ok=True)

    lines = parse_dialogue(script_text)

    for idx, (character, text) in enumerate(lines):
        voice_id = CHARACTER_VOICES.get(character.upper())
        if voice_id:
            output_file = Path(output_dir) / f"{character.lower()}_line{idx+1}.mp3"
            generate_voice(text, str(output_file), voice_id)
        else:
            print(f"[!] No voice assigned for character: {character}")

# Example usage
process_script("script.md", "voice_clips")