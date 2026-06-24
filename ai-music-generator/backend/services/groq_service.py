import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

async def generate_with_groq(prompt: str, system_message: str = None) -> str:
    if not os.getenv("GROQ_API_KEY"):
        return "❌ GROQ_API_KEY is missing in .env file"

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_message or "You are a creative assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=1200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Groq Error:", e)
        return f"Groq Error: {str(e)}"


async def generate_lyrics_with_groq(topic: str, genre: str = "Afrobeat", flow_style: str = "Energetic", structure: str = "Full Song"):
    system_prompt = f"""You are a world-class {genre} songwriter with exceptional flow and cultural authenticity.
Write emotional, catchy, and rhythmic lyrics that sound professional and radio-ready."""

    user_prompt = f"""Create high-quality original song lyrics:

Topic: {topic}
Genre: {genre}
Desired Flow: {flow_style}
Structure: {structure}

Rules for excellence:
- Strong storytelling and vivid imagery
- Catchy, repeatable chorus
- Natural rhyme scheme that matches {genre} rhythm
- Use slang/pidgin where appropriate for authenticity
- Make it emotional and memorable"""

    return await generate_with_groq(user_prompt, system_prompt)

# For Beat Blueprint
async def generate_beat_blueprint(genre: str, mood: str, tempo: str = "", key: str = "", notes: str = ""):
    prompt = f"""Create a detailed beat blueprint for a {genre} song with a {mood} mood.

Tempo: {tempo}
Key: {key}
Extra notes: {notes}

Use these sections:
🥁 DRUM PATTERN
🎹 MELODY & CHORDS
🎸 INSTRUMENTS
🎚️ ARRANGEMENT
💡 PRODUCTION TIPS"""
    
    system = "You are a world-class music producer."
    return await generate_with_groq(prompt, system)