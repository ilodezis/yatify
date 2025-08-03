# core.py — ядро переноса плейлистов
from yandex_api import fetch_playlist_tracks
from spotify_api import SpotifyTransfer
import os
import json

TOKEN_FILE = "token.json"

def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_token(token_data):
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(token_data, f, ensure_ascii=False, indent=2)

def transfer_playlist(yandex_url, client_id, client_secret, redirect_uri, playlist_name=None, log_func=None):
    """
    Основная функция переноса: загружает треки из ЯМ, авторизует Spotify, создаёт плейлист, добавляет треки.
    log_func — функция для логирования (может быть None)
    """
    if log_func is None:
        log_func = print
    log_func("Получение треков из Яндекс.Музыки...")
    tracks = fetch_playlist_tracks(yandex_url)
    if not tracks:
        raise Exception("Не удалось получить треки из Яндекс.Музыки")
    log_func(f"Найдено треков: {len(tracks)}")
    # Авторизация Spotify
    transfer = SpotifyTransfer(client_id, client_secret, redirect_uri, token_file=TOKEN_FILE)
    # Создание плейлиста
    if playlist_name is None:
        playlist_name = "Yatify Imported Playlist"
    log_func(f"Создание плейлиста Spotify: {playlist_name}")
    playlist_id = transfer.create_playlist(playlist_name)
    log_func(f"[core] Создан плейлист: {playlist_id}")
    # Добавление треков
    for tname in tracks:
        try:
            result = transfer.add_track_to_playlist(playlist_id, tname)
        except Exception as e:
            log_func(f"[!] Ошибка при добавлении: {tname} — {e}")
            continue
        if result == "added":
            log_func(f"[+] Добавлен: {tname}")
        elif result == "notfound":
            log_func(f"[!] Не найден: {tname}")
    log_func("Готово!")
    return playlist_id
