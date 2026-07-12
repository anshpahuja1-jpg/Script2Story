# pdf_builder.py
# Assembles scene images into a storyboard PDF

from PIL import Image, ImageDraw


def build_storyboard_pdf(scenes, images, output_path):
    page_width = 1240
    page_height = 1754
    margin = 40
    padding = 20

    cell_width = (page_width - 2 * margin - padding) // 2
    cell_height = 320
    caption_height = 80
    row_height = cell_height + caption_height + padding

    def new_page():
        page = Image.new("RGB", (page_width, page_height), color=(245, 245, 240))
        draw = ImageDraw.Draw(page)
        draw.rectangle([0, 0, page_width, 80], fill=(30, 30, 30))
        draw.text((margin, 25), "SCRIPT2STORY — AI STORYBOARD", fill=(255, 255, 255))
        return page, draw

    pages = []
    current_page, draw = new_page()
    row = 0

    for i, (scene, img) in enumerate(zip(scenes, images)):
        col = i % 2
        if i > 0 and col == 0:
            row += 1

        if row > 0 and row % 2 == 0 and col == 0:
            pages.append(current_page)
            current_page, draw = new_page()
            row = 0

        x = margin + col * (cell_width + padding)
        y = 100 + row * row_height

        resized = img.resize((cell_width, cell_height))
        current_page.paste(resized, (x, y))

        caption_y = y + cell_height
        draw.rectangle([x, caption_y, x + cell_width, caption_y + caption_height],
                       fill=(30, 30, 30))
        draw.text((x + 10, caption_y + 8),
                  f"Scene {i+1}  |  {scene['shot_type']}", fill=(255, 220, 100))
        draw.text((x + 10, caption_y + 30), scene["heading"][:50], fill=(200, 200, 200))
        short_desc = scene["description"][:60] + "..." if len(scene["description"]) > 60 else scene["description"]
        draw.text((x + 10, caption_y + 52), short_desc, fill=(150, 150, 150))

    pages.append(current_page)

    pages[0].save(
        output_path,
        save_all=True,
        append_images=pages[1:],
        resolution=150
    )
    print(f"  Saved to: {output_path}")
