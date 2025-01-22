import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyClient:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="user-top-read"
        ))
    
    def get_top_tracks(self, limit=5):
        try:
            results = self.sp.current_user_top_tracks(limit=limit)
            top_tracks = []
            for track in results['items']:
                top_tracks.append({
                    'name': track['name'],
                    'artist': ', '.join(artist['name'] for artist in track['artists']),
                    'album': track['album']['name'],
                    'url': track['external_urls']['spotify']
                })
            return top_tracks
        except Exception as e:
            print(f"Cannot get songs: {e}")
            return []