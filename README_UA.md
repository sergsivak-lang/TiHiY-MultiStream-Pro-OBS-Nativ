# TiHiY MultiStream Pro v2.2 ACTIVE START BUTTONS

Нативний OBS-плагін для одночасного стріму на YouTube / Twitch / Custom RTMP.

## Головне у v2.2

- RutonyChat прибрано повністю.
- Автовідкриття чатів при старті прибрано.
- Панель компактна.
- Додано видимий стан запуску для всіх Start-кнопок.
- Після натискання Start кнопка показує `Starting...`, потім `LIVE`.
- При помилці показує `START FAILED`, `CREATE FAILED` або `MISSING SERVER / KEY`.
- У кожному вікні YouTube / Twitch / Custom є окремий статус.
- У головній панелі є загальний статус `IDLE` або `LIVE — YouTube + Twitch`.

## Панель

- Start All
- Stop All
- YouTube
- Twitch
- Custom
- Save settings
- Recommended settings
- Twitch safe 1080 fix
- Status: IDLE / LIVE

## Рекомендовані налаштування

- YouTube: 2560×1440, 60 FPS, 24000 Kbps.
- Twitch: 1920×1080, 60 FPS, 6000 Kbps.
- Twitch safe 1080 fix: ON.

## Інсталятор

Після GitHub Actions можна встановити вручну або зібрати Setup.exe:

- `tools/INSTALL_PLUGIN_SIMPLE.bat`
- `tools/MAKE_INSTALLER_FROM_ACTIONS_ARTIFACT.bat`

За замовчуванням інсталятор орієнтується на OBS у:

`F:\OOBS\obs-studio`
