from pydantic import BaseModel
from typing import Optional

class LyricsRequest(BaseModel):
    topic: str
    language: str = "English"
    structure: str = "Verse-Chorus-Verse-Chorus-Bridge-Chorus"

class LyricsResponse(BaseModel):
    lyrics: str
    topic: str

class MusicRequest(BaseModel):
    genre: str
    mood: str
    tempo: str = "90-110 BPM"
    key: str = "C Major"
    notes: Optional[str] = None

class MusicResponse(BaseModel):
    blueprint: str
    genre: str