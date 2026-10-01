from fpdf import FPDF
from PIL import Image
import os


def export_comic_to_pdf(image_path):
    """
    Convert the generated comic image into a PDF.
    """

    if not image_path or not os.path.exists(image_path):
        return None

    os.makedirs("static/exports", exist_ok=True)

    pdf_path = "static/exports/comic.pdf"

    image = Image.open(image_path)

    width, height = image.size

    pdf = FPDF(
        orientation="P",
        unit="pt",
        format=(width, height)
    )

    pdf.add_page()

    pdf.image(
        image_path,
        x=0,
        y=0,
        w=width,
        h=height
    )

    pdf.output(pdf_path)

    return pdf_path