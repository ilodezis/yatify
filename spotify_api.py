import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import json

class SpotifyTransfer:
    def __init__(self, client_id, client_secret, redirect_uri, token_file=None):
        self.token_file = token_file
        self.auth_manager = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="playlist-modify-public playlist-modify-private user-library-modify user-library-read"
        )
        if token_file and os.path.exists(token_file):
            with open(token_file, "r", encoding="utf-8") as f:
                token_info = json.load(f)
            self.auth_manager.cache_handler.save_token_to_cache(token_info)
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)
        # Сохраняем токен после авторизации
        if token_file:
            token_info = self.auth_manager.cache_handler.get_cached_token()
            if token_info:
                with open(token_file, "w", encoding="utf-8") as f:
                    json.dump(token_info, f, ensure_ascii=False, indent=2)

    def add_track(self, artist_and_title: str) -> str:
        res = self.sp.search(q=artist_and_title, type="track", limit=1)
        items = res["tracks"]["items"]
        if not items:
            return "notfound"
        track_id = items[0]["id"]
        already = self.sp.current_user_saved_tracks_contains([track_id])[0]
        if already:
            return "already"
        self.sp.current_user_saved_tracks_add([track_id])
        return "added"

    def create_playlist(self, name):
        user = self.sp.current_user()["id"]
        pl = self.sp.user_playlist_create(user, name, public=False)
        return pl["id"]

    def add_track_to_playlist(self, playlist_id, artist_and_title):
        res = self.sp.search(q=artist_and_title, type="track", limit=1)
        items = res["tracks"]["items"]
        if not items:
            return "notfound"
        track_id = items[0]["id"]
        self.sp.user_playlist_add_tracks(self.sp.current_user()["id"], playlist_id, [track_id])
        return "added"
