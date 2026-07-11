# TiHiY MultiStream Pro v1.7 — Compact Scalable Panel

Що змінилось:

- панель стала компактною і краще масштабується в OBS dock;
- зверху тепер поруч кнопки **Start All** і **Stop All**;
- нижче кнопки **YouTube**, **Twitch**, **Custom**;
- налаштування платформ більше не займають всю висоту панелі;
- при натисканні **YouTube / Twitch / Custom** відкривається окреме вікно налаштувань;
- окремо винесені кнопки **Save settings** і **Recommended settings**;
- збереження ключів і параметрів залишилось;
- Twitch Safe 1080 Fix залишився увімкненим за замовчуванням.

Як оновити:

1. Розпакуй архів.
2. У GitHub template-repo натисни **Add file → Upload files**.
3. Завантаж весь вміст розпакованої папки, не ZIP.
4. **Commit changes**.
5. **Actions → дочекайся Windows artifact**.
6. Закрий OBS.
7. Заміни `F:\OOBS\obs-studio\obs-plugins\64bit\tihiy-multistream-pro.dll`.
8. Запусти OBS.

Після запуску має бути компактна панель:

Start All | Stop All
YouTube | Twitch | Custom
Save settings | Recommended settings



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
