# parser.py
def parse_script(filepath):
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
    text_lower = text.lower()

    # Angle based
    if "worm" in text_lower or "ground level" in text_lower:
        return "WORM'S EYE VIEW"
    if "bird" in text_lower or "overhead" in text_lower or "aerial" in text_lower or "drone" in text_lower:
        return "BIRD'S EYE VIEW"
    if "low angle" in text_lower or "looking up" in text_lower:
        return "LOW ANGLE SHOT"
    if "high angle" in text_lower or "looking down" in text_lower:
        return "HIGH ANGLE SHOT"
    if "dutch" in text_lower or "tilted" in text_lower:
        return "DUTCH ANGLE"
    if "pov" in text_lower or "point of view" in text_lower or "first person" in text_lower:
        return "POV SHOT"

    # Framing based
    if "extreme close" in text_lower or "eye" in text_lower or "detail" in text_lower:
        return "EXTREME CLOSE-UP"
    if "close" in text_lower or "face" in text_lower:
        return "CLOSE-UP"
    if "reaction" in text_lower or "expression" in text_lower:
        return "REACTION SHOT"
    if "shoulder" in text_lower or "conversation" in text_lower or "dialogue" in text_lower:
        return "OVER-THE-SHOULDER"
    if "medium" in text_lower or "waist" in text_lower:
        return "MEDIUM SHOT"

    # Movement
    if "walk" in text_lower or "runs" in text_lower or "follows" in text_lower or "chase" in text_lower:
        return "TRACKING SHOT"

    # Wide
    if "vast" in text_lower or "landscape" in text_lower or "horizon" in text_lower:
        return "EXTREME WIDE SHOT"
    if "city" in text_lower or "street" in text_lower or "rooftop" in text_lower or "crowd" in text_lower:
        return "WIDE SHOT"

    # Default
    if "alone" in text_lower or "elevator" in text_lower or "room" in text_lower:
        return "MEDIUM SHOT"

    return "ESTABLISHING SHOT"