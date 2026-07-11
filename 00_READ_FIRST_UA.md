# TiHiY MultiStream Pro — важливо перед завантаженням

Цей пакет НЕ треба заливати в старий репозиторій, який був створений вручну.
Старий репозиторій падає на `OBS::libobs`, бо він не має повної системи OBS Plugin Template.

Правильний шлях:

1. Створити НОВИЙ репозиторій через офіційний `obsproject/obs-plugintemplate` кнопкою `Use this template`.
2. У новому template-репозиторії залишити службові файли шаблону.
3. Завантажити вміст цього overlay-пакета поверх template-репозиторію.
4. Не створювати вручну `.github/workflows/main.yml`.
5. Запускати workflow, який уже є в OBS Plugin Template.

## Що вже враховано

- Твій OBS 32.1.2.
- Твоя відеокарта NVIDIA RTX 5060 Ti.
- NVENC H.264 encoder id: `obs_nvenc_h264_tex`.
- Конфлікт `obs-multi-rtmp` вже треба тримати вимкненим.
- Потрібна збірка саме native OBS plugin `.dll`, а не Lua script.
- GitHub Actions має використовувати template build system, а не саморобний workflow.

## Що НЕ робити

- Не створювати порожній `main.yml` вручну.
- Не заливати цей пакет у старий repo без OBS Plugin Template.
- Не видаляти папки `.github/actions`, `.github/scripts`, `build-aux`, `cmake`, `CMakePresets.json`, `buildspec.json` із template repo.


## v1.3 Twitch Safe Fix
- Додано Twitch safe 1080 fix: x264 fallback для Twitch 1080p, коли OBS canvas 2560x1440.
- Додано кнопку Apply recommended 2K YouTube + 1080 Twitch.
- Додано Save settings для локального збереження серверів/ключів/бітрейтів.
