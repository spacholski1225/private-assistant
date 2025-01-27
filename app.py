import base64
from urllib.parse import urlencode
from dotenv import load_dotenv
from flask import Flask, redirect, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import spotipy
import spotipy.util as util
import speech_recognition as sr
import os
import tempfile
import subprocess
import time
import agent
from tools.spotify import SpotifyClient
import helpers.tts_helper as tts

app = Flask(__name__, static_folder='static')
CORS(app)
load_dotenv()

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/login')
def login():
    scope = 'user-read-private user-read-email'
    auth_url = f"https://accounts.spotify.com/authorize?client_id={os.getenv("SPOTIFY_CLIENT_ID")}&response_type=code&redirect_uri={os.getenv("SPOTIFY_REDIRECT_URI")}&scope={scope}"
    return redirect(auth_url)

@app.route("/callback")
def callback():
    """
    Endpoint obsługujący przekierowanie z Spotify. Wymienia kod na token dostępowy.
    """
    code = request.args.get("code")

    if code is None:
        return "Brak kodu autoryzacyjnego w żądaniu.", 400

    auth_options = {
        'url': 'https://accounts.spotify.com/api/token',
        'data': {
            'code': code,
            'redirect_uri': os.getenv("SPOTIFY_REDIRECT_URI"),
            'grant_type': 'authorization_code'
        },
        'headers': {
            'content-type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + base64.b64encode(f"{os.getenv("SPOTIFY_CLIENT_ID")}:{os.getenv("SPOTIFY_CLIENT_SECRET")}".encode()).decode()
        }
    }

    response = requests.post(auth_options['url'], data=auth_options['data'], headers=auth_options['headers'])
    token_info = response.json()

    if response.status_code != 200:
        return f"Błąd podczas wymiany kodu na token: {token_info.get('error_description', 'Nieznany błąd')}", 400

    access_token = token_info["access_token"]
    
    # Zainicjalizowanie klienta Spotify z tokenem
    global spotify
    spotify = spotipy.Spotify(auth=access_token)
    print('Autoryzacja zakończona sukcesem! Możesz teraz używać API.')

    return "Autoryzacja zakończona sukcesem! Możesz teraz używać API.", 200



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
            print(f"Recognize text: {text}")

            answer = agent.Agent.ask_agent(text)
            print(f"Agent answer: {answer}")
            
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
        print(f"Error occurs: {str(e)}")
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