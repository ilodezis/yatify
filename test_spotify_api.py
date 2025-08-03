# test_spotify_api.py
import pytest
from spotify_api import SpotifyTransfer

class DummySpotify:
    def __init__(self):
        self.saved = set()
        self.playlists = {}
    def search(self, q, type, limit):
        # Возвращаем фиктивный трек
        if q == 'Artist1 – Song1':
            return {"tracks": {"items": [{"id": "track1"}]}}
        return {"tracks": {"items": []}}
    def current_user_saved_tracks_contains(self, ids):
        return [id in self.saved for id in ids]
    def current_user_saved_tracks_add(self, ids):
        self.saved.update(ids)
    def user_playlist_create(self, user, name, public):
        pid = f"pl_{name}"
        self.playlists[pid] = []
        return {"id": pid}
    def user_playlist_add_tracks(self, user, pid, track_ids):
        self.playlists[pid].extend(track_ids)

@pytest.fixture
def dummy_transfer(monkeypatch):
    monkeypatch.setattr('spotify_api.spotipy.Spotify', lambda *a, **kw: DummySpotify())
    monkeypatch.setattr('spotify_api.SpotifyOAuth', lambda *a, **kw: None)
    return SpotifyTransfer('id', 'secret', 'uri')

def test_add_track(dummy_transfer):
    assert dummy_transfer.add_track('Artist1 – Song1') == 'added'
    assert dummy_transfer.add_track('Artist1 – Song1') == 'already'
    assert dummy_transfer.add_track('Unknown – SongX') == 'notfound'
