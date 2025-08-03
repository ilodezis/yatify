# cli.py — командная строка для переноса плейлистов
import argparse
from core import transfer_playlist

def main():
    parser = argparse.ArgumentParser(description="Yatify CLI: перенос плейлистов из Яндекс.Музыки в Spotify")
    parser.add_argument('--yandex-url', required=True, help='Ссылка на плейлист Яндекс.Музыки')
    parser.add_argument('--spotify-client-id', required=True, help='Spotify Client ID')
    parser.add_argument('--spotify-secret', required=True, help='Spotify Client Secret')
    parser.add_argument('--redirect-uri', default='http://127.0.0.1:8080', help='Spotify Redirect URI')
    parser.add_argument('--playlist-name', default=None, help='Название нового плейлиста Spotify')
    args = parser.parse_args()

    def log(msg):
        print(msg)

    try:
        playlist_id = transfer_playlist(
            args.yandex_url,
            args.spotify_client_id,
            args.spotify_secret,
            args.redirect_uri,
            playlist_name=args.playlist_name,
            log_func=log
        )
        print(f'Готово! ID плейлиста Spotify: {playlist_id}')
    except Exception as e:
        print(f'[ERROR] {e}')

if __name__ == "__main__":
    main()
