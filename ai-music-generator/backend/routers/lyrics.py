from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import Optional
import librosa
import numpy as np
import io

from services.groq_service import generate_lyrics_with_groq

router = APIRouter(prefix="/api/lyrics")

class LyricsRequest(BaseModel):
    topic: str
    genre: str = "Afrobeat"
    flow_style: str = "Energetic"
    structure: str = "Full Song"

class LyricsResponse(BaseModel):
    lyrics: str
    topic: str
    genre: str


@router.post("/generate", response_model=LyricsResponse)
async def generate_lyrics(request: LyricsRequest):
    lyrics_text = await generate_lyrics_with_groq(
        topic=request.topic,
        genre=request.genre,
        flow_style=request.flow_style,
        structure=request.structure
    )
    return LyricsResponse(lyrics=lyrics_text, topic=request.topic, genre=request.genre)


# ====================== UPLOAD BEAT + BPM ANALYSIS ======================
@router.post("/from-beat")
async def generate_from_beat(
    file: UploadFile = File(...),
    genre: str = "Afrobeat",
    flow_style: str = "Energetic",
    notes: Optional[str] = ""
):
    try:
        contents = await file.read()
        filename = file.filename

        # Audio Analysis with proper type conversion
        y, sr = librosa.load(io.BytesIO(contents), sr=None)
        
        # Fixed BPM detection
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        bpm = int(round(float(tempo))) if tempo is not None else 0
        
        # Energy calculation
        energy = float(np.mean(librosa.feature.rms(y=y)[0]))
        energy_level = "high" if energy > 0.12 else "medium" if energy > 0.06 else "low"

        topic = f"Beat: {filename} | BPM: {bpm} | Energy: {energy_level} | {notes or 'Create catchy and rhythmic lyrics'}"

        lyrics_text = await generate_lyrics_with_groq(
            topic=topic,
            genre=genre,
            flow_style=flow_style,
            structure="Full Song"
        )

        return {
            "lyrics": lyrics_text,
            "filename": filename,
            "bpm": bpm,
            "energy": energy_level,
            "message": f"✅ Generated for {filename} ({bpm} BPM, {energy_level} energy)"
        }

    except Exception as e:
        print("Beat Processing Error:", str(e))
        return {"error": f"Failed to process beat: {str(e)}"}