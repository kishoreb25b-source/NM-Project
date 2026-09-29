import os


def generate_panel_image(
    panel_number,
    description,
    art_style="Digital Comic Art"
):
    """
    Return an existing comic panel.
    """

    file_path = f"static/panels/panel_{panel_number}.png"

    if os.path.exists(file_path):
        return file_path

    raise FileNotFoundError(
        f"Panel image not found: {file_path}"
    )