import os
import base64
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

app = FastAPI(title="Google AI Music Generator")

# static 폴더 경로 설정 (없으면 생성)
os.makedirs("static", exist_ok=True)

class MusicRequest(BaseModel):
    genre: str
    bpm_key: str
    mood: str
    vocal: str

@app.post("/api/generate")
async def generate_music(req: MusicRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=400, 
            detail="GEMINI_API_KEY가 설정되지 않았습니다. .env 파일을 확인해 주세요."
        )

    prompt = f"""
    장르 & 악기: {req.genre}
    BPM & 키: {req.bpm_key}
    무드: {req.mood}
    보컬 여부: {req.vocal}
    """

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="lyria-3-pro-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO", "TEXT"],
            ),
        )

        lyrics = []
        audio_base64 = None
        audio_bytes = None

        for part in response.parts:
            if part.text is not None:
                lyrics.append(part.text)
            elif part.inline_data is not None:
                audio_bytes = part.inline_data.data
                audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

        # 파일로도 저장 (요청 시 최신 저장 목적)
        if audio_bytes:
            with open("static/latest_clip.mp3", "wb") as f:
                f.write(audio_bytes)

        return {
            "success": True,
            "lyrics": "\n".join(lyrics) if lyrics else "생성된 가사가 없습니다.",
            "audio": audio_base64
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# static 파일 마운트
app.mount("/", StaticFiles(directory="static", html=True), name="static")
