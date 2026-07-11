# TiHiY MultiStream Pro v1.4 — START ALL + Twitch Safe Fix

Що нового:

- додано кнопку **Start All** поруч із **Stop All**;
- Start All запускає всі увімкнені виходи у безпечному порядку: YouTube → Twitch → Custom;
- перед Start All автоматично зберігаються налаштування/ключі через QSettings;
- залишено Twitch Safe 1080 Fix із v1.3;
- пресет: YouTube 2K60 + Twitch 1080p60.

Як оновити:

1. Розпакуй архів.
2. У GitHub template repo натисни **Add file → Upload files**.
3. Завантаж весь вміст розпакованої папки, не сам ZIP.
4. Commit changes.
5. Actions → дочекайся Windows artifact.
6. Закрий OBS.
7. Заміни `F:\OOBS\obs-studio\obs-plugins\64bit\tihiy-multistream-pro.dll`.
8. Запусти OBS.

Рекомендовано: спочатку натисни **Apply recommended 2K YouTube + 1080 Twitch**, встав ключі, натисни **Save settings**, потім тестуй **Start All**.
