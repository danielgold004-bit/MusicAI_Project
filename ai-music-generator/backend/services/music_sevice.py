import os
import json
import httpx
from dotenv import load_dotenv

load_dotenv()

FAL_API_KEY = os.getenv("FAL_API_KEY")

async def generate_music_with_fal(prompt: str, duration: int = 30):
    if not FAL_API_KEY:
        return "❌ FAL_API_KEY not found in .env file"
    
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "https://queue.fal.run/fal-ai/flux-music",
                headers={
                    "Authorization": f"Key {FAL_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "prompt": prompt,
                    "duration": duration,
                    "format": "mp3"
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "audio_url": result.get("audio_url"),
                    "status": "success"
                }
            else:
                return f"Error: {response.text}"
    except Exception as e:
        return f"Failed to generate music: {str(e)}"