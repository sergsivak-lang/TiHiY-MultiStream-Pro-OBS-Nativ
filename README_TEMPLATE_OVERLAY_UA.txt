TiHiY MultiStream Pro TEMPLATE OVERLAY v1.3

Цей пакет враховує попередні помилки GitHub Actions:
- Visual Studio runner issue
- Qt6 missing
- OBS::libobs target missing

Головне рішення: використовувати не старий repo, а НОВИЙ repo, створений через obsproject/obs-plugintemplate.

Коротко:
1. Create new repo from obsproject/obs-plugintemplate.
2. Upload this overlay into that repo.
3. Keep template service folders.
4. Run template Actions.
5. Download artifact with native OBS plugin.


## v1.3 Twitch Safe Fix
- Додано Twitch safe 1080 fix: x264 fallback для Twitch 1080p, коли OBS canvas 2560x1440.
- Додано кнопку Apply recommended 2K YouTube + 1080 Twitch.
- Додано Save settings для локального збереження серверів/ключів/бітрейтів.
