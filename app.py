from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import speech_recognition as sr
import os
import tempfile
import subprocess
import time
import agent
import tools.tts_tool as tts

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file'}), 400
    
    audio_file = request.files['audio']
    webm_path = None
    wav_path = None
    audio_response_path = None
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_webm:
            webm_path = temp_webm.name
            audio_file.save(webm_path)
        
        wav_path = webm_path + '.wav'
        subprocess.run(['ffmpeg', '-i', webm_path, wav_path], check=True)
        
        time.sleep(0.1)
        
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='pl-PL')
            print(f"Rozpoznany tekst: {text}")

            answer = agent.Agent.ask_agent(text)
            print(f"Odpowiedź agenta: {answer}")
            
            audio_response_path = tts.text_to_speech_file(answer)
            
            with open(audio_response_path, 'rb') as audio_file:
                audio_data = audio_file.read()
                import base64
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                
            return jsonify({
                'success': True,
                'text': answer,
                'audio_data': audio_base64
            })
            
    except Exception as e:
        print(f"Wystąpił błąd: {str(e)}")
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500
    finally:
        for path in [webm_path, wav_path, audio_response_path]:
            if path and os.path.exists(path):
                try:
                    os.close(os.open(path, os.O_RDONLY))
                    os.unlink(path)
                except Exception as e:
                    print(f"Cannot delete file {path}: {e}")

if __name__ == '__main__':
    app.run(debug=True)