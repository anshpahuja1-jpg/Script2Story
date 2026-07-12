# image_generator.py
import time
import requests
from PIL import Image, ImageDraw
from io import BytesIO
import textwrap
import os

REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN", "")
def build_prompt(scene):
    shot_descriptions = {
        "CLOSE-UP": "extreme close-up shot, face filling frame, shallow depth of field, bokeh background, 50mm lens",
        "WIDE SHOT": "wide angle establishing shot, vast environment, small human figure, 24mm lens, sweeping vista",
        "TRACKING SHOT": "dynamic tracking shot, motion blur, following subject, handheld camera feel, cinematic movement",
        "MEDIUM SHOT": "medium shot, waist up framing, rule of thirds, natural headroom, 35mm lens",
        "ESTABLISHING SHOT": "establishing shot, full environment visible, architectural detail, location context, 28mm lens",
        "OVER-THE-SHOULDER": "over the shoulder shot, foreground subject blurred, focus on background subject, depth",
    }
    shot_detail = shot_descriptions.get(scene['shot_type'], "cinematic shot, 35mm lens")
    prompt = (
        f"{shot_detail}, "
        f"cinematic color grading, "
        f"{scene['heading'].lower()}, "
        f"{scene['description']}, "
        f"professional film cinematography, anamorphic lens flare, "
        f"dramatic chiaroscuro lighting, deep shadows, film grain, "
        f"movie still, high budget production, 4k, photorealistic"
    )
    return prompt

def fetch_image(prompt, retries=3):
    headers = {
        "Authorization": f"Bearer {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json",
        "Prefer": "wait"
    }
    for attempt in range(retries):
        try:
            print(f"    Generating image (attempt {attempt + 1})...")
            response = requests.post(
                "https://api.replicate.com/v1/models/black-forest-labs/flux-dev/predictions",
                headers=headers,
                json={
                    "input": {
                        "prompt": prompt,
                        "width": 1024,
                        "height": 576,
                        "num_outputs": 1
                    }
                },
                timeout=180
            )
            if response.status_code in [200, 201]:
                result = response.json()
                while result.get("status") not in ["succeeded", "failed"]:
                    time.sleep(3)
                    poll = requests.get(
                        result["urls"]["get"],
                        headers=headers,
                        timeout=30
                    )
                    result = poll.json()
                if result.get("status") == "succeeded":
                    image_url = result["output"][0]
                    img_response = requests.get(image_url, timeout=30)
                    img = Image.open(BytesIO(img_response.content))
                    return img
                else:
                    print(f"    Failed: {result.get('error')}")
            else:
                print(f"    Error {response.status_code}: {response.text[:150]}")
                time.sleep(5)
        except Exception as e:
            print(f"    Exception: {e}")
            time.sleep(5)
    return None

def generate_fallback_image(scene, scene_index):
    COLORS = [(44,62,80),(39,55,70),(28,40,51),(52,73,94),(93,63,106)]
    img = Image.new("RGB", (800, 450), color=COLORS[scene_index % len(COLORS)])
    draw = ImageDraw.Draw(img)
    draw.rectangle([10,10,790,440], outline=(255,255,255), width=2)
    draw.text((30,30), f"SCENE {scene_index+1}", fill=(200,200,200))
    draw.text((30,60), f"[ {scene['shot_type']} ]", fill=(255,220,100))
    draw.text((30,110), scene["heading"], fill=(255,255,255))
    wrapped = textwrap.wrap(scene["description"], width=70)
    y = 160
    for line in wrapped[:6]:
        draw.text((30,y), line, fill=(180,180,180))
        y += 28
    return img

def generate_image(scene, scene_index):
    prompt = build_prompt(scene)
    print(f"  Prompt: {prompt[:100]}...")
    img = fetch_image(prompt)
    if img:
        print(f"  ✓ Real AI image generated")
        return img
    else:
        print(f"  ✗ Failed, using placeholder")
        return generate_fallback_image(scene, scene_index)