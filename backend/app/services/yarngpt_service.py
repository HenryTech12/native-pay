"""
YarnGPT — Nigerian-accented text-to-speech, used for the confirmation/
read-back voice in place of the browser's generic speechSynthesis. Voice
selection is per our supported language codes; YarnGPT has no dedicated
Pidgin voice yet, so Pidgin falls back to the English voice.

https://yarngpt.ai/api-docs
"""

import os
import httpx

YARNGPT_BASE_URL = os.environ.get("YARNGPT_BASE_URL", "https://yarngpt.ai/api/v1")
YARNGPT_API_KEY = os.environ.get("YARNGPT_API_KEY")

VOICE_BY_LANGUAGE = {
    "en": "idera",
    "pcm": "idera",  # no dedicated Pidgin voice yet — closest available
    "yo": "abayomi",
    "ha": "amina",
    "ig": "chioma",
}


async def synthesize_speech(text: str, language: str) -> bytes:
    if not YARNGPT_API_KEY:
        raise RuntimeError("YARNGPT_API_KEY not configured")

    voice = VOICE_BY_LANGUAGE.get(language, "idera")
    async with httpx.AsyncClient(timeout=30) as client:
        res = await client.post(
            f"{YARNGPT_BASE_URL}/tts",
            headers={"Authorization": f"Bearer {YARNGPT_API_KEY}"},
            json={"text": text, "voice": voice, "response_format": "mp3"},
        )
        res.raise_for_status()
        return res.content
