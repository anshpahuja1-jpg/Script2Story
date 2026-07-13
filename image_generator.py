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
        # Basic shots
        "CLOSE-UP": "close-up shot, face filling frame, shallow depth of field, bokeh background, 50mm lens, emotional intimacy",
        "EXTREME CLOSE-UP": "extreme close-up shot, single detail filling entire frame, macro lens, intense emphasis, 100mm macro lens",
        "MEDIUM SHOT": "medium shot, waist up framing, rule of thirds, natural headroom, 35mm lens, balanced composition",
        "WIDE SHOT": "wide angle shot, full subject visible with environment, 24mm lens, sense of scale and location",
        "EXTREME WIDE SHOT": "extreme wide shot, tiny subject in vast environment, 16mm lens, sweeping landscape, isolation",

        # Angle shots
        "LOW ANGLE SHOT": "low angle shot, camera looking up at subject, subject feels powerful and dominant, dramatic perspective, 28mm lens",
        "HIGH ANGLE SHOT": "high angle shot, camera looking down at subject, subject feels small and vulnerable, overhead perspective",
        "BIRD'S EYE VIEW": "bird's eye view, straight overhead shot, top down perspective, reveals layout and scale, drone shot aesthetic",
        "WORM'S EYE VIEW": "worm's eye view, extreme low angle, camera on ground looking up, subject feels towering and dominant, ultra wide lens",
        "EYE LEVEL SHOT": "eye level shot, camera at subject's eye height, natural balanced perspective, neutral emotional tone, 35mm lens",

        # Movement and technique
        "TRACKING SHOT": "tracking shot, camera following subject in motion, subtle motion blur, dynamic movement, cinematic dolly",
        "OVER-THE-SHOULDER": "over the shoulder shot, foreground figure blurred, focus on background subject, dialogue framing, depth",
        "POV SHOT": "point of view shot, camera becomes character's eyes, first person perspective, immersive, handheld feel",
        "DUTCH ANGLE": "dutch tilt shot, camera tilted 15 degrees, psychological tension, unease and disorientation, thriller aesthetic",

        # Establishing
        "ESTABLISHING SHOT": "establishing shot, full environment visible, architectural detail, sets location and context, 28mm lens",
        "REACTION SHOT": "reaction shot, character's emotional response, subtle facial expression, 85mm portrait lens, shallow focus",
    }

    shot_detail = shot_descriptions.get(
        scene['shot_type'],
        "cinematic shot, 35mm lens, professional cinematography"
    )

    prompt = (
        f"{shot_detail}, "
        f"cinematic color grading, "
        f"{scene['heading'].lower()}, "
        f"{scene['description']}, "
        f"professional film cinematography, anamorphic lens flare, "
        f"dramatic chiaroscuro lighting, deep shadows, film grain, "
        f"movie still, high budget production, 4k, photorealistic, "
        f"shot on 35mm film, Kodak Vision3"
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
                        "num_outputs": 1,
                        "num_inference_steps": 28,
                        "guidance_scale": 3.5
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
        except requests.exceptions.Timeout:
            print(f"    Timed out. Retrying...")
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