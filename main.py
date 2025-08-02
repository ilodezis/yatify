import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, QMessageBox, QComboBox, QInputDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from yandex_api import fetch_playlist_tracks
from spotify_api import SpotifyTransfer

SETTINGS_FILE = os.path.join(os.path.expanduser("~"), ".yatify_settings.json")

TRANSLATIONS = {
    'ru': {
        'title': 'Yatify — перенос плейлистов из Яндекс Музыки в Spotify',
        'yandex_url': 'Ссылка на плейлист Яндекс Музыки:',
        'client_id': 'Spotify Client ID:',
        'client_secret': 'Spotify Client Secret:',
        'redirect_uri': 'Spotify Redirect URI:',
        'import': 'Импортировать в Spotify',
        'help': 'Инструкция',
        'log': 'Лог импорта:',
        'fill_all': "<span style='color:red;'>[!] Заполните все поля!</span>",
        'import_start': '<b>Импорт начинается...</b>',
        'not_found': "<span style='color:red;'>[!] Не удалось получить треки. Проверьте ссылку.</span>",
        'found': 'Найдено треков: {}',
        'added': "<span style='color:green;'>[+] Добавлен: {}</span>",
        'already': "[=] Уже был: {}",
        'notfound': "<span style='color:orange;'>[!] Не найден: {}</span>",
        'done': '<b>\nГотово!</b>',
        'error_tracks': "<span style='color:red;'>[!] Не удалось получить треки: {}</span>",
        'error_add': "<span style='color:red;'>[!] Ошибка при добавлении: {} — {}</span>",
        'help_title': 'Инструкция',
        'help_text': '''<b>Пошаговая инструкция для переноса плейлиста из Яндекс.Музыки в Spotify:</b><br><br>
1. <b>Откройте Яндекс.Музыку</b> в браузере и перейдите на страницу нужного плейлиста.<br><br>
2. <b>Скопируйте ссылку и вставьте её в первое поле приложения.</b><br><br>
3. <b>Зайдите на сайт <a href='https://developer.spotify.com/dashboard/applications'>Spotify Developer Dashboard</a></b>.<br>
   - Войдите в свой аккаунт Spotify.<br>
   - Нажмите "Create an App" и заполните название и описание.<br>
   - После создания приложения скопируйте Client ID и Client Secret.<br><br>
4. <b>Вставьте Client ID и Client Secret</b> в соответствующие поля.<br><br>
5. <b>В настройках приложения Spotify</b> добавьте Redirect URI: <b>http://127.0.0.1:8080</b> (или используйте этот URI по умолчанию).<br>
   - Скопируйте этот URI и вставьте в поле Spotify Redirect URI.<br><br>
6. <b>Нажмите кнопку "Импортировать в Spotify"</b>.<br><br>
7. <b>Дождитесь завершения процесса</b>. Внизу появится лог с результатами по каждому треку.<br><br>''',
        'lang': 'Язык:',
    },
    'en': {
        'title': 'Yatify — transfer playlists from Yandex Music to Spotify',
        'yandex_url': 'Yandex Music playlist URL:',
        'client_id': 'Spotify Client ID:',
        'client_secret': 'Spotify Client Secret:',
        'redirect_uri': 'Spotify Redirect URI:',
        'import': 'Import to Spotify',
        'help': 'Help',
        'log': 'Import log:',
        'fill_all': "<span style='color:red;'>[!] Please fill in all fields!</span>",
        'import_start': '<b>Import started...</b>',
        'not_found': "<span style='color:red;'>[!] Could not get tracks. Check the link.</span>",
        'found': 'Tracks found: {}',
        'added': "<span style='color:green;'>[+] Added: {}</span>",
        'already': "[=] Already exists: {}",
        'notfound': "<span style='color:orange;'>[!] Not found: {}</span>",
        'done': '<b>\nDone!</b>',
        'error_tracks': "<span style='color:red;'>[!] Could not get tracks: {}</span>",
        'error_add': "<span style='color:red;'>[!] Error adding: {} — {}</span>",
        'help_title': 'Help',
        'help_text': '''<b>Step-by-step guide to transfer a playlist from Yandex Music to Spotify:</b><br><br>
1. <b>Open Yandex Music</b> in your browser and go to the desired playlist page.<br><br>
2. <b>Copy the link and paste it into the first field of the app.</b><br><br>
3. <b>Go to <a href='https://developer.spotify.com/dashboard/applications'>Spotify Developer Dashboard</a></b>.<br>
   - Log in to your Spotify account.<br>
   - Click "Create an App" and fill in the name and description.<br>
   - After creating the app, copy the Client ID and Client Secret.<br><br>
4. <b>Paste Client ID and Client Secret</b> into the corresponding fields.<br><br>
5. <b>In your Spotify app settings</b> add Redirect URI: <b>http://127.0.0.1:8080</b> (or use this URI by default).<br>
   - Copy this URI and paste it into the Spotify Redirect URI field.<br><br>
6. <b>Click the "Import to Spotify" button</b>.<br><br>
7. <b>Wait for the process to finish</b>. The log with results for each track will appear below.<br><br>''',
        'lang': 'Language:',
    }
}

class YatifyGUI(QWidget):
    def __init__(self, language):
        super().__init__()
        self.language = language
        self.setWindowTitle(TRANSLATIONS[self.language]['title'])
        self.setMinimumWidth(540)
        self.setStyleSheet("""
            QWidget {
                background: #23272e;
                color: #e0e0e0;
            }
            QLabel {
                color: #bfc7d5;
                font-size: 15px;
                margin-bottom: 2px;
            }
            QLineEdit {
                background: #2c313a;
                color: #e0e0e0;
                border: 1px solid #444b58;
                border-radius: 5px;
                padding: 7px 10px;
                font-size: 15px;
                margin-bottom: 10px;
            }
            QPushButton {
                font-weight: 600;
                font-size: 15px;
                background: #3a7afe;
                color: #fff;
                border: none;
                border-radius: 6px;
                padding: 10px 18px;
                margin: 0 4px 10px 0;
                transition: background 0.2s;
            }
            QPushButton:hover {
                background: #2554c7;
            }
            QTextEdit {
                background: #181a20;
                color: #bfc7d5;
                border-radius: 6px;
                font-size: 14px;
                padding: 10px;
            }
        """)
        self.settings = self.load_settings()
        self.init_ui()

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_settings(self):
        data = {
            "yandex_url": self.yandex_url.text(),
            "client_id": self.client_id.text(),
            "client_secret": self.client_secret.text(),
            "redirect_uri": self.redirect_uri.text()
        }
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def init_ui(self):
        t = TRANSLATIONS[self.language]
        layout = QVBoxLayout()
        layout.setSpacing(8)
        # Yandex
        layout.addWidget(QLabel(t['yandex_url']))
        self.yandex_url = QLineEdit(self.settings.get("yandex_url", ""))
        layout.addWidget(self.yandex_url)
        # Spotify
        layout.addWidget(QLabel(t['client_id']))
        self.client_id = QLineEdit(self.settings.get("client_id", ""))
        layout.addWidget(self.client_id)
        layout.addWidget(QLabel(t['client_secret']))
        self.client_secret = QLineEdit(self.settings.get("client_secret", ""))
        layout.addWidget(self.client_secret)
        layout.addWidget(QLabel(t['redirect_uri']))
        self.redirect_uri = QLineEdit(self.settings.get("redirect_uri", "http://127.0.0.1:8080"))
        layout.addWidget(self.redirect_uri)
        # Buttons
        btn_layout = QHBoxLayout()
        self.import_btn = QPushButton(t['import'])
        self.import_btn.clicked.connect(self.import_playlist)
        btn_layout.addWidget(self.import_btn)
        self.help_btn = QPushButton(t['help'])
        self.help_btn.setStyleSheet("background: #2554c7; color: #fff; font-weight: 600; font-size: 15px; border-radius: 6px; padding: 10px 18px; margin: 0 4px 10px 0;")
        self.help_btn.clicked.connect(self.show_help)
        btn_layout.addWidget(self.help_btn)
        layout.addLayout(btn_layout)
        # Log
        layout.addWidget(QLabel(t['log']))
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setStyleSheet("background: #181a20; color: #bfc7d5; border-radius: 6px; font-size: 14px; padding: 10px;")
        layout.addWidget(self.log)
        self.setLayout(layout)

    def log_message(self, msg):
        self.log.append(msg)

    def import_playlist(self):
        t = TRANSLATIONS[self.language]
        self.save_settings()
        yandex_url = self.yandex_url.text().strip()
        client_id = self.client_id.text().strip()
        client_secret = self.client_secret.text().strip()
        redirect_uri = self.redirect_uri.text().strip()
        if not all([yandex_url, client_id, client_secret, redirect_uri]):
            self.log_message(t['fill_all'])
            return
        self.log_message(t['import_start'])
        try:
            tracks = fetch_playlist_tracks(yandex_url)
        except Exception as e:
            self.log_message(t['error_tracks'].format(e))
            return
        if not tracks:
            self.log_message(t['not_found'])
            return
        self.log_message(t['found'].format(len(tracks)))
        transfer = SpotifyTransfer(client_id, client_secret, redirect_uri)
        for tname in tracks:
            try:
                result = transfer.add_track(tname)
            except Exception as e:
                self.log_message(t['error_add'].format(tname, e))
                continue
            if result == "added":
                self.log_message(t['added'].format(tname))
            elif result == "already":
                self.log_message(t['already'].format(tname))
            elif result == "notfound":
                self.log_message(t['notfound'].format(tname))
        self.log_message(t['done'])

    def show_help(self):
        t = TRANSLATIONS[self.language]
        msg = QMessageBox(self)
        msg.setWindowTitle(t['help_title'])
        msg.setText(t['help_text'])
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

def main():
    # Language selection at startup
    app = QApplication(sys.argv)
    lang, ok = QInputDialog.getItem(None, "Language / Язык", "Choose language / Выберите язык:", ["Русский", "English"], 0, False)
    language = 'ru' if lang == 'Русский' else 'en'
    gui = YatifyGUI(language)
    gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
