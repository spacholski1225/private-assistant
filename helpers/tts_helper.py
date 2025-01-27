import os
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
import tempfile
ELEVENLABS_API_KEY = os.getenv("EVENLABS_KEY")

if not ELEVENLABS_API_KEY:
    raise ValueError("EVENLABS_KEY is not set!")

client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)

def text_to_speech_file(text: str) -> str:
    if not ELEVENLABS_API_KEY:
        raise ValueError("Missing evenlabs key!")
        
    try:
        response = client.text_to_speech.convert(
            voice_id="pNInz6obpgDQGcFmaJgB", #default voice
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
        print(f"Error Evenlabs API: {str(e)}")
        raise