from PIL import Image, ImageDraw
import os


def build_comic_layout(panel_paths):
    """
    Arrange comic panels vertically into one comic page.
    """

    if not panel_paths:
        return None

    images = []

    for path in panel_paths:
        if os.path.exists(path):
            images.append(Image.open(path).convert("RGB"))

    if not images:
        return None

    panel_width = 800
    panel_height = 500
    gap = 20

    total_height = (
        len(images) * panel_height
        + (len(images) - 1) * gap
    )

    comic = Image.new(
        "RGB",
        (panel_width, total_height),
        "white"
    )

    y = 0

    for image in images:
        image = image.resize(
            (panel_width, panel_height)
        )

        comic.paste(image, (0, y))

        y += panel_height + gap

    os.makedirs("static/exports", exist_ok=True)

    output_path = "static/exports/comic_layout.png"

    comic.save(output_path)

    return output_path