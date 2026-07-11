# TiHiY MultiStream Pro v1.7

Native OBS-плагін для окремого multistream на YouTube / Twitch / Custom RTMP з різними роздільностями та бітрейтами.

## Головне у v1.7

- компактна OBS dock-панель;
- панель масштабується краще і не займає велику висоту;
- **Start All** і **Stop All** поряд зверху;
- кнопки **YouTube / Twitch / Custom** відкривають окремі вікна налаштувань;
- **Save settings** і **Recommended settings** винесені на головну панель;
- Twitch Safe 1080 Fix збережено;
- stream keys зберігаються через QSettings у профілі Windows-користувача.

## Рекомендований пресет

- OBS canvas/output: 2560x1440 / 60 FPS
- YouTube: 2560x1440 / 60 FPS / 24000 Kbps
- Twitch: 1920x1080 / 60 FPS / 6000 Kbps



## v1.7 AUTO OPEN CHATS

- Додано автоматичне відкриття чатів після старту YouTube/Twitch/Custom.
- У вікнах YouTube/Twitch/Custom зʼявились поля `Chat URL` і `Open chat after start`.
- На головній компактній панелі додано кнопку `Open chats`.
- Twitch за замовчуванням має popout-chat URL для `tihiy_ded`; YouTube за замовчуванням відкриває YouTube Studio, а точний popout chat URL можна вставити вручну.
- Stream keys і Chat URLs зберігаються через `Save settings`.


## v1.7 RutonyChat Launcher
- Додано кнопку Rutony Chat у компактну панель.
- Можна вибрати шлях до RutonyChat.exe.
- Можна запускати RutonyChat вручну або автоматично після старту трансляції.
- Додано Start Rutony / Stop Rutony.

Майбутній етап: TiHiY Chat — власний аналог RutonyChat для Twitch + YouTube з ботом та імпортом налаштувань Rutony.
