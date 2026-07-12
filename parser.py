# parser.py
# Reads the screenplay and breaks it into scenes

def parse_script(filepath):
    """
    Reads a screenplay file and returns a list of scenes.
    Each scene is a dict with:
      - heading: the scene heading (e.g. INT. COFFEE SHOP - DAY)
      - description: the action/description text
      - shot_type: guessed shot type based on content
    """
    with open(filepath, "r") as f:
        content = f.read()

    blocks = [b.strip() for b in content.strip().split("\n\n") if b.strip()]

    scenes = []
    current_scene = None

    for block in blocks:
        first_line = block.split("\n")[0].strip()

        if first_line.startswith("INT.") or first_line.startswith("EXT."):
            if current_scene:
                scenes.append(current_scene)
            current_scene = {
                "heading": first_line,
                "description": "\n".join(block.split("\n")[1:]).strip(),
                "shot_type": guess_shot_type(block)
            }
        else:
            if current_scene:
                current_scene["description"] += " " + block

    if current_scene:
        scenes.append(current_scene)

    return scenes


def guess_shot_type(text):
    text = text.lower()
    if "close" in text or "face" in text or "eyes" in text:
        return "CLOSE-UP"
    elif "wide" in text or "city" in text or "street" in text or "rooftop" in text:
        return "WIDE SHOT"
    elif "walk" in text or "enters" in text or "moves" in text:
        return "TRACKING SHOT"
    elif "elevator" in text or "alone" in text:
        return "MEDIUM SHOT"
    else:
        return "ESTABLISHING SHOT"
