import io
import os

import requests
import re
import json

from pydub import AudioSegment

ELEVENLABS_API_KEY = os.environ["ELEVENLABS_API_KEY"]
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Example: 'Rachel' voice
voices_map = {
    "RILEY": "21m00Tcm4TlvDq8ikWAM",
    "JAMIE": "29vD33N1CtxCmqQRPOHJ"
}

def generate_voice(text, voice_id):
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
        # with open(output_filename, "wb") as f:
        #     f.write(response.content)
        # print(f"Audio saved to {output_filename}")
        print("Success")
        return response.content
    else:
        print("Error:", response.status_code, response.text)
        return "Nothing"


script = """
**RILEY**
*(softly, unsure)*  
"...Hey."

*JAMIE's eyes snap to Riley, surprise etching their features.*

**JAMIE**  
*(blinking, disbelieving)*  
"...Riley?"

*Riley nods, a small, awkward smile forming as they shift the weight of their bags, as if trying to find balance in this unexpected encounter.*

**RILEY**  
"Yeah. It's been a while."

*JAMIE sets the coffee cup down on the bench, their demeanor a blend of skepticism and old hurt.*

**JAMIE**  
"A while? That's… generous. Try five years."

**RILEY**  
*(with a wistfulness)*  
"Feels shorter."

**JAMIE**  
"Feels longer."

*Silence slips in, tethered to unspoken words and shared history. Riley places the bags down, uncertainty in every movement.*

**RILEY**  
"I just moved back."
"""

pattern = r"\*\*(.*?)\*\*\s*(?:\*.*?\*\s*)*(?:\(.*?\)\s*)*([\"“].*?[\"”])"
matches = re.findall(pattern, script, re.DOTALL)

dialogue_list = []
for char, line in matches:
    clean_line = re.sub(r'[\*]+', '', line)
    clean_line = re.sub(r'\(.*?\)', '', clean_line)
    clean_line = clean_line.strip()
    dialogue_list.append({
        "character": char.strip(),
        "voice": voices_map.get(char.strip(), None),
        "line": clean_line
    })

final_scene = AudioSegment.silent(duration=500)  # small pause before start

for entry in dialogue_list:
    if not entry["voice"]:
        print(f"⚠ No voice ID for {entry['character']}, skipping...")
        continue
    print(f"🎙 {entry['character']}: {entry['line']}")
    audio_bytes = generate_voice(entry["line"], entry["voice"])
    audio_segment = AudioSegment.from_mp3(io.BytesIO(audio_bytes))
    final_scene += audio_segment + AudioSegment.silent(duration=300)

# === STEP 4: Export the Scene ===
final_scene.export("scene_output.mp3", format="mp3")
print("✅ Scene audio saved as scene_output.mp3")
# generate_voice(clean_script, "speech.mp3")