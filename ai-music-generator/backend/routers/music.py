from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from services.groq_service import generate_beat_blueprint

router = APIRouter(prefix="/api/music")  # ← was /music, missing /api

class MusicRequest(BaseModel):
    genre: str
    mood: str
    tempo: str = "mid-tempo (85–100 BPM)"
    key: str = "C Major"
    notes: Optional[str] = None

class MusicResponse(BaseModel):
    blueprint: str


@router.post("/generate", response_model=MusicResponse)
async def generate_music(request: MusicRequest):
    blueprint = await generate_beat_blueprint(
        genre=request.genre,
        mood=request.mood,
        tempo=request.tempo,
        key=request.key,
        notes=request.notes or ""
    )
    return MusicResponse(blueprint=blueprint)