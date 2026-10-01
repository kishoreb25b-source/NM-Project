import os

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.gemini_flash import generate_comic_outline
from app.gemini_pro import generate_narration
from app.image_generator import generate_panel_image
from app.layout_builder import build_comic_layout
from app.exporters import export_comic_to_pdf


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@router.post("/generate", response_class=HTMLResponse)
async def generate_comic(
    request: Request,
    story: str = Form(...),
    character: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...)
):

    try:

        # Step 1: Generate comic outline
        outline_result = generate_comic_outline(
            story,
            character,
            setting,
            tone,
            art_style
        )

        if "outline" not in outline_result:
            return HTMLResponse(
                content=f"<h2>Gemini Error</h2><pre>{outline_result}</pre>",
                status_code=500
            )

        # Step 2: Generate narration and dialogue
        narration_result = generate_narration(
            outline_result["outline"]
        )

        if "narration" not in narration_result:
            return HTMLResponse(
                content=f"<h2>Gemini Error</h2><pre>{narration_result}</pre>",
                status_code=500
            )

        # Step 3: Get comic panels
        panel_paths = []

        for panel_number in range(1, 6):

            existing_panel = (
                f"static/panels/panel_{panel_number}.png"
            )

            if os.path.exists(existing_panel):

                panel_paths.append(existing_panel)

            else:

                panel_description = f"""
Create the visual scene for Panel {panel_number} of this comic.

Main Character:
{character}

Setting:
{setting}

Story Tone:
{tone}

Art Style:
{art_style}

The complete comic outline is:
{outline_result['outline']}

The narration and dialogue are:
{narration_result['narration']}

Focus specifically on Panel {panel_number}.
Show the characters, actions, setting, and important objects
that belong to this panel.
Do not show events from other panels.
"""

                panel_path = generate_panel_image(
                    panel_number,
                    panel_description,
                    art_style
                )

                panel_paths.append(panel_path)

        # Step 4: Build comic layout
        comic_layout = build_comic_layout(
            panel_paths
        )

        # Step 5: Export PDF
        pdf_path = export_comic_to_pdf(
            comic_layout
        )

        # Step 6: Show preview
        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "story": story,
                "character": character,
                "setting": setting,
                "tone": tone,
                "art_style": art_style,
                "outline": outline_result,
                "narration": narration_result,
                "comic_layout": comic_layout,
                "pdf_path": pdf_path
            }
        )

    except Exception as e:

        return HTMLResponse(
            content=f"<h2>Application Error</h2><pre>{str(e)}</pre>",
            status_code=500
        )