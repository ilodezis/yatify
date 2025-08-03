from yandex_music import Client
import re
from typing import List

def fetch_playlist_tracks(playlist_url: str) -> List[str]:
    """
    Берёт ссылку вида https://music.yandex.ru/users/USERNAME/playlists/PLAYLIST_ID
    Возвращает список строк "Исполнитель – Название".
    """
    m = re.match(r"https?://music\.yandex\.ru/users/([^/]+)/playlists/(\d+)", playlist_url)
    if not m:
        raise ValueError("Некорректная ссылка на плейлист Яндекс.Музыки")
    user, playlist_id = m.group(1), m.group(2)
    client = Client().init()  # public API, без авторизации
    try:
        pl = client.users_playlists(playlist_id, user)
        if not pl or not hasattr(pl, 'tracks'):
            raise Exception("Плейлист не найден или приватный")
        result = []
        for t in pl.tracks:
            artist = t.track.artists[0].name if t.track.artists else "Unknown Artist"
            title  = t.track.title
            result.append(f"{artist} – {title}")
        return result
    except Exception as e:
        raise Exception(f"Ошибка при получении треков: {e}")
