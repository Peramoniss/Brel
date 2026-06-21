from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from langdetect import detect
from deep_translator import GoogleTranslator
from pydantic import BaseModel


ENV = os.getenv(key="ENV", default="DEV")

app = FastAPI(
    title="Songs Translator API",
    description="Year-end lists and all-time artist rankings",
    version="1.0.0"
)

origins = ["https://peramoniss.github.io"]
if ENV == "DEV":
    new_origins = [
        "http://localhost:3000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://127.0.0.1:8000",
    ]
    for no in new_origins: #origins.extend(new_origins), but my brain is too low-level to allow something like that
        origins.append(no)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    print("Healthy")
    return {"status": "ok"}

class TranslationRequest(BaseModel):
    lyrics: str
    lang: str
    strat: str

@app.post("/translate/")
def translate(req: TranslationRequest):
    TARGET_LANG = req.lang
    STRATEGY = req.strat
    lyrics = req.lyrics

    if req.strat not in {"verse", "stanza", "whole"}:
        raise HTTPException(
            status_code=400,
            detail="Strategy must be verse, stanza, or whole"
        )

    src_lang = detect(req.lyrics)
    translator = GoogleTranslator(
        source=src_lang,
        target=TARGET_LANG
    )

    def __translate(text: str) -> str:
        if not text.strip():
            return ""
        try:
            return translator.translate(text)
        except Exception as e:
            # fallback: keep original if translation fails
            return text

    # -----------------------------
    # Translate lines
    # -----------------------------
    rows = []
    if STRATEGY == "verse":
        for line in lyrics.splitlines():
            translated = __translate(line)
            rows.append((line, translated))
    elif STRATEGY == "stanza":
        for stanza in lyrics.split("\n\n"):
            translated_stanza = __translate(stanza)
            for line, translated in zip(stanza.splitlines(), translated_stanza.splitlines()):
                rows.append((line, translated))
            rows.append(("", ""))
    elif STRATEGY == "whole":
        translated_lyrics = __translate(lyrics)
        for line, translated in zip(lyrics.splitlines(), translated_lyrics.splitlines()):
            rows.append((line, translated))
    
    return rows