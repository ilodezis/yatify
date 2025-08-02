import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyTransfer:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="user-library-modify user-library-read"
        ))

    def add_track(self, artist_and_title: str) -> str:
        res = self.sp.search(q=artist_and_title, type="track", limit=1)
        items = res["tracks"]["items"]
        if not items:
            return "notfound"
        track_id = items[0]["id"]
        # Проверяем, есть ли уже в "Мне нравится"
        already = self.sp.current_user_saved_tracks_contains([track_id])[0]
        if already:
            return "already"
        self.sp.current_user_saved_tracks_add([track_id])
        return "added"
