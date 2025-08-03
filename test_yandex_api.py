# test_yandex_api.py
import pytest
from yandex_api import fetch_playlist_tracks

def test_fetch_playlist_tracks(monkeypatch):
    # Мокаем ответ клиента Яндекс.Музыки
    class DummyTrack:
        def __init__(self, artist, title):
            self.track = type('T', (), {'artists': [type('A', (), {'name': artist})], 'title': title})
    class DummyPlaylist:
        def __init__(self):
            self.tracks = [DummyTrack('Artist1', 'Song1'), DummyTrack('Artist2', 'Song2')]
    def dummy_users_playlists(pid, user):
        return DummyPlaylist()
    class DummyClient:
        def init(self): return self
        def users_playlists(self, pid, user): return dummy_users_playlists(pid, user)
    monkeypatch.setattr('yandex_api.Client', lambda: DummyClient())
    tracks = fetch_playlist_tracks('https://music.yandex.ru/users/test/playlists/123')
    assert tracks == ['Artist1 – Song1', 'Artist2 – Song2']
