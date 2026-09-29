import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


def generate_narration(outline):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {
            "error": "GEMINI_API_KEY is not configured."
        }

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are a comic dialogue and narration writer.

Using the following comic outline, create narration and dialogue
for each panel.

Comic outline:
{outline}

For each panel, provide:
1. Panel number
2. Short narration
3. Short character dialogue

Keep the dialogue natural, simple, and suitable for a comic.
Do not make the text too long.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return {
        "narration": response.text
    }