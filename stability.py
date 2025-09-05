import requests
from PIL import Image
from io import BytesIO
import os

STABILITY_API_KEY = os.environ["STABILITY_AI_API_KEY"]

def generate_scene_image(prompt, output_filename, width=768, height=512):
    """
    Generate an image from a scene description using Stability AI's text-to-image API.
    """
    url = "https://api.stability.ai/v2beta/stable-image/generate/core"

    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "image/png"
    }

    payload = {
        "prompt": prompt,
        "output_format": "png",
        "width": width,
        "height": height,
        "mode": "text-to-image"
    }

    response = requests.post(url, headers=headers, files={"none": ''}, data=payload)

    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img.save(output_filename)
        print(f"[✓] Image saved: {output_filename}")
    else:
        print("[!] Error:", response.status_code, response.text)


scene_descriptions = [
    "A dark laboratory with flickering lights, a small robot awakening on a metal table",
    "A dim underground tunnel with red emergency lights",
    "A bright open field with green grass and a blue sky",
    "A small bird perches on the robot's metallic hand"
]

os.makedirs("scene_images", exist_ok=True)

for idx, scene in enumerate(scene_descriptions, start=1):
    generate_scene_image(scene, f"scene_images/scene_{idx}.png")