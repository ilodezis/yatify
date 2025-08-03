# <img src="icon.icns" width="32" height="32"/> Yatify

**RU | [EN](#english)**

Yatify — перенос плейлистов из Яндекс.Музыки в Spotify с помощью современного GUI (PyQt5) или CLI.

## Структура проекта
- `gui.py` — графический интерфейс (PyQt5)
- `cli.py` — командная строка (argparse)
- `core.py` — ядро переноса (логика)
- `yandex_api.py` — работа с Яндекс.Музыкой
- `spotify_api.py` — работа со Spotify, хранение токенов в `token.json`
- `test_yandex_api.py`, `test_spotify_api.py` — тесты (pytest, mock)
- `pyproject.toml` — зависимости и точки входа
- `icon.icns` — иконка приложения

## Быстрый старт
1. Установите зависимости:
   ```sh
   pip install -r requirements.txt
   ```
2. Запустите GUI:
   ```sh
   python gui.py
   ```
   или CLI:
   ```sh
   python cli.py --yandex-url "<url>" --spotify-client-id "..." --spotify-secret "..." --redirect-uri "..."
   ```
3. Токены Spotify сохраняются в `token.json` (повторная авторизация не требуется).

## Тесты
```sh
pytest
```

## Сборка standalone-приложения
```sh
pyinstaller --onedir --windowed --icon=icon.icns gui.py
```

## Релизы
- [Windows](https://github.com/ilodezis/yatify/releases)
- [macOS](https://github.com/ilodezis/yatify/releases)

---

# <a name="english"></a><img src="icon.icns" width="32" height="32"/> Yatify

Yatify — transfer playlists from Yandex Music to Spotify with a modern GUI (PyQt5) or CLI.

## Project structure
- `gui.py` — graphical interface (PyQt5)
- `cli.py` — command line (argparse)
- `core.py` — transfer engine (logic)
- `yandex_api.py` — Yandex Music API
- `spotify_api.py` — Spotify API, tokens in `token.json`
- `test_yandex_api.py`, `test_spotify_api.py` — tests (pytest, mock)
- `pyproject.toml` — dependencies and entry points
- `icon.icns` — app icon

## Quick start
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run GUI:
   ```sh
   python gui.py
   ```
   or CLI:
   ```sh
   python cli.py --yandex-url "<url>" --spotify-client-id "..." --spotify-secret "..." --redirect-uri "..."
   ```
3. Spotify tokens are saved in `token.json` (no repeated authorization required).

## Tests
```sh
pytest
```

## Build standalone app
```sh
pyinstaller --onedir --windowed --icon=icon.icns gui.py
```

## Releases
- [Windows](https://github.com/ilodezis/yatify/releases)
- [macOS](https://github.com/ilodezis/yatify/releases)
