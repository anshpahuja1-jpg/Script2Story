# main.py
# Run this file to generate your storyboard
# Usage: python main.py

from parser import parse_script
from image_generator import generate_image
from pdf_builder import build_storyboard_pdf

SCRIPT_PATH = "script.txt"   # change this to your own script file
OUTPUT_PATH = "storyboard.pdf"


def main():
    print("=" * 50)
    print("  SCRIPT2STORY — AI Storyboard Generator")
    print("=" * 50)

    # STEP 1: Parse the script
    print("\n[1/3] Parsing script...")
    scenes = parse_script(SCRIPT_PATH)
    print(f"  Found {len(scenes)} scenes:\n")
    for i, scene in enumerate(scenes):
        print(f"  Scene {i+1}: {scene['heading']} ({scene['shot_type']})")

    # STEP 2: Generate images
    print("\n[2/3] Generating images...")
    images = []
    for i, scene in enumerate(scenes):
        print(f"\n  Scene {i+1}: {scene['heading']}")
        img = generate_image(scene, i)
        images.append(img)

    # STEP 3: Build PDF
    print("\n[3/3] Building storyboard PDF...")
    build_storyboard_pdf(scenes, images, OUTPUT_PATH)

    print("\n✓ Done! Open storyboard.pdf to see your storyboard.")
    print("=" * 50)


if __name__ == "__main__":
    main()
