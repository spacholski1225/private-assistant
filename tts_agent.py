from flask import send_file
import os
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
import tempfile
ELEVENLABS_API_KEY = os.getenv("EVENLABS_KEY")

# Sprawdź czy klucz API istnieje
if not ELEVENLABS_API_KEY:
    raise ValueError("EVENLABS_KEY nie jest ustawiony w zmiennych środowiskowych!")

# Inicjalizacja klienta z explicit sprawdzeniem klucza
client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)

def text_to_speech_file(text: str) -> str:
    if not ELEVENLABS_API_KEY:
        raise ValueError("Brak klucza API ElevenLabs")
        
    try:
        response = client.text_to_speech.convert(
            voice_id="pNInz6obpgDQGcFmaJgB",
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_turbo_v2_5",
            voice_settings=VoiceSettings(
                stability=0.0,
                similarity_boost=1.0,
                style=0.0,
                use_speaker_boost=True,
            ),
        )
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            for chunk in response:
                if chunk:
                    temp_file.write(chunk)
            return temp_file.name
            
    except Exception as e:
        print(f"Błąd ElevenLabs API: {str(e)}")
        raise