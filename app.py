from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import speech_recognition as sr
import os
import tempfile
import subprocess
import time
import agent

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
            print(text)

            answer = agent.Agent.ask_agent(text)

            print(answer)

            return jsonify({
                'success': True,
                'text': answer
            })
            
    except sr.UnknownValueError:
        return jsonify({'error': 'Cannot recognize audio'}), 400
    except sr.RequestError as e:
        return jsonify({'error': f'Service error: {str(e)}'}), 500
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Cannot convert audio: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500
    finally:
        try:
            if webm_path and os.path.exists(webm_path):
                os.close(os.open(webm_path, os.O_RDONLY))
                os.unlink(webm_path)
        except Exception as e:
            print(f"Cannot delete file webm: {e}")
            
        try:
            if wav_path and os.path.exists(wav_path):
                os.close(os.open(wav_path, os.O_RDONLY))
                os.unlink(wav_path)
        except Exception as e:
            print(f"Cannot delete file wav: {e}")

if __name__ == '__main__':
    app.run(debug=True)