import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


def generate_comic_outline(story, character, setting, tone, art_style):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {
            "error": "GEMINI_API_KEY is not configured."
        }

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are a comic story planner.

Convert the following story into a 5-panel comic outline.

Story:
{story}

Main character:
{character}
Setting:
{setting}
Tone:
{tone}
Art style:
{art_style}

For each panel, provide:
1. Panel number
2. Scene description
3. Character action
4. Short dialogue or narration

Keep the output simple and suitable for generating comic images.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return {
        "outline": response.text
    }