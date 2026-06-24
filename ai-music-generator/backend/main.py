from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Music Studio")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import all routers
from routers.lyrics import router as lyrics_router
from routers.music import router as music_router

# Register them
app.include_router(lyrics_router)
app.include_router(music_router)

@app.get("/")
async def root():
    return {
        "status": "✅ Running",
        "endpoints": [
            "/api/lyrics/generate",
            "/api/music/generate",
            "/api/lyrics/from-beat"
        ]
    }

print("🚀 AI Music Studio Backend Started Successfully!")