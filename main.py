import elevenlabs
import openai
import requests
import re
import os

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
ELEVENLABS_API_KEY = os.environ["ELEVENLABS_API_KEY"]
# Placeholder for image/video and music API keys
STABILITY_AI_API_KEY = os.environ["STABILITY_AI_API_KEY"]
SUNO_AI_API_KEY = os.environ["SUNO_AI_API_KEY"]

# --- Step 1: Script Generation using OpenAI ---
def generate_script(storyline):
    """Generates a simple script from a storyline."""
    print("🎬 Generating script...")
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a professional screenwriter. Write a very short, single-scene script with one character and a clear scene description. Include dialogue and scene descriptions."},
            {"role": "user", "content": f"Storyline: {storyline}"}
        ]
    )
    script = response.choices[0].message.content
    print("✅ Script generated:\n", script)
    return script

def extract_visual_description_and_dialogue(script):
    """Extract visual description and dialogue from the generated script."""
    print("🔍 Extracting visual description and dialogue from script...")
    
    # Ask OpenAI to extract the key elements
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Extract from the script: 1) A detailed visual description for image generation (max 100 words), 2) The main dialogue text (max 200 words). Return in format: VISUAL: [description] DIALOGUE: [dialogue]"},
            {"role": "user", "content": f"Script: {script}"}
        ]
    )
    
    extracted = response.choices[0].message.content
    
    # Parse the response
    visual_match = re.search(r'VISUAL:\s*(.*?)(?=DIALOGUE:|$)', extracted, re.DOTALL)
    dialogue_match = re.search(r'DIALOGUE:\s*(.*?)(?=VISUAL:|$)', extracted, re.DOTALL)
    
    visual_description = visual_match.group(1).strip() if visual_match else "A dramatic scene with characters"
    dialogue_text = dialogue_match.group(1).strip() if dialogue_match else "Hello, this is a test."
    
    print(f"✅ Visual description: {visual_description[:100]}...")
    print(f"✅ Dialogue text: {dialogue_text[:100]}...")
    
    return visual_description, dialogue_text

# --- Step 2: Visual Asset Generation ---
def generate_image_from_text(description):
    """Generate an image from text using Stability AI's API."""
    print("🖼️ Generating image from description...")

    # Load API key from environment variable
    api_key = STABILITY_AI_API_KEY
    if not api_key:
        raise ValueError("Missing STABILITY_AI_API_KEY environment variable.")

    # API endpoint and headers
    url = "https://api.stability.ai/v2beta/stable-image/generate/core"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "image/png"
    }

    payload = {
        "prompt": description
    }

    # Send request
    response = requests.post(url, headers=headers, json=payload)

    # Check for errors
    if response.status_code != 200:
        raise RuntimeError(f"Image generation failed: {response.text}")

    # Save image
    image_path = "scene_image.png"
    with open(image_path, "wb") as f:
        f.write(response.content)

    print(f"✅ Image saved to {image_path}")
    return image_path

# --- Step 3: Dialogue Generation using ElevenLabs ---
def generate_dialogue_audio(text, voice_id="21m00Tcm4TlvDq8ikWAM"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    output_filename = "eleven_audio.mp3"
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
        print(f"Audio saved to {output_filename}")
    else:
        print("Error:", response.status_code, response.text)

# --- Step 4: Music Generation (Placeholder) ---
def generate_music(mood):
    """Placeholder function for music generation."""
    print("🎶 Generating background music...")
    # This is a placeholder. In a real app, you would call a music generation API
    print("✅ Music generated (using placeholder).")
    return "placeholder_music.mp3"

# --- Step 5: Video Assembly (Simplified) ---
def assemble_video_simple(image_path, dialogue_audio_path, music_audio_path=None):
    """Simple video assembly using basic tools."""
    print("🎞️ Assembling video (simplified)...")
    
    try:
        # For now, just create a simple text file with instructions
        output_path = "video_assembly_instructions.txt"
        with open(output_path, "w") as f:
            f.write("VIDEO ASSEMBLY INSTRUCTIONS\n")
            f.write("=" * 30 + "\n\n")
            f.write(f"1. Image file: {image_path}\n")
            f.write(f"2. Dialogue audio: {dialogue_audio_path}\n")
            if music_audio_path:
                f.write(f"3. Music audio: {music_audio_path}\n")
            f.write("\nTo create the final video:\n")
            f.write("- Use a video editor like DaVinci Resolve, Premiere Pro, or even online tools\n")
            f.write("- Import the image and set it as the video track\n")
            f.write("- Import the dialogue audio and sync it with the image\n")
            f.write("- Add the music as background audio (lower volume)\n")
            f.write("- Export as MP4\n")
        
        print(f"✅ Video assembly instructions saved to {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ Error creating assembly instructions: {str(e)}")
        return None

# --- Main execution flow ---
def main():
    """Main function to generate a complete movie from storyline."""
    print("🎬 Starting AI Movie Generation Pipeline...")
    
    # Your storyline
    storyline = """
    Jamie sat hunched over a paper cup of coffee, pretending to read the ripples on the lake. They didn't notice Riley at first—not until the sound of grocery bags brushing together broke through the stillness.
    
    Riley stopped a few feet away, hesitant. Should I say something? It had been five years, after all.
    
    Riley: "…Hey."
    Jamie: (looking up, startled) "…Riley?"
    Riley: "Yeah. It's been a while."
    Jamie: "A while? That's… generous. Try five years."
    Riley: "Feels shorter."
    Jamie: "Feels longer."
    
    Riley set the groceries down, shifting their weight like they weren't sure if they were staying or leaving.
    
    Riley: "I just moved back."
    Jamie: "Why?"
    Riley: "Job ended. Relationship ended. Everything just… ended. So here I am."
    Jamie: (quietly) "You always said you'd never come back."
    Riley: "I know."
    Jamie: "So what changed?"
    Riley: "…I think I realized I left some things here I didn't want to leave."
    
    Jamie looked away at the lake. The wind rippled it in small, uneven waves.
    
    Jamie: "Well. The bookstore's still there."
    Riley: "I wasn't talking about the bookstore."
    
    There was a silence that carried more than either of them was ready to unpack.
    
    Jamie: "…You should probably get those groceries home before the ice cream melts."
    Riley: "Yeah. Maybe I'll see you around?"
    Jamie: "Maybe."
    
    Riley picked up the bags and walked away, but Jamie didn't turn to watch them go.
    """
    
    try:
        # Step 1: Generate script
        script = generate_script(storyline)
        
        # Step 2: Extract visual description and dialogue
        visual_description, dialogue_text = extract_visual_description_and_dialogue(script)
        
        # Step 3: Generate image
        # image_path = generate_image_from_text(visual_description)
        
        # Step 4: Generate dialogue audio
        dialogue_audio_path = generate_dialogue_audio(dialogue_text)
        
        # Step 5: Generate music (optional)
        music_audio_path = generate_music("Emotional and contemplative")
        image_path = "scene_image.png"
        # Step 6: Create assembly instructions
        instructions_path = assemble_video_simple(image_path, dialogue_audio_path, music_audio_path)
        
        if instructions_path:
            print(f"🎉 Movie generation complete! Check the generated files:")
            print(f"   - Image: {image_path}")
            print(f"   - Audio: {dialogue_audio_path}")
            print(f"   - Instructions: {instructions_path}")
        else:
            print("❌ Movie generation failed!")
            
    except Exception as e:
        print(f"❌ Error in movie generation pipeline: {str(e)}")

if __name__ == "__main__":
    main()