# TiHiY MultiStream Pro v2.2 ACTIVE START BUTTONS

Це чиста версія без Rutony і без автовідкриття чатів.

Додано головне виправлення:
- після натискання будь-якої кнопки Start видно стан запуску;
- Start показує `Starting...`;
- після успішного старту кнопка стає `LIVE`;
- у вікні платформи видно статус `READY / STARTING / LIVE / STOPPED / ERROR`;
- у головній панелі видно `Status: IDLE` або `Status: LIVE — YouTube + Twitch`;
- `Start All` теж показує активний стан.

## Правильний порядок

1. Завантаж весь вміст цієї папки в GitHub repo через **Add file → Upload files**.
2. Саме в repo: `sergsivak-lang/TiHiY-MultiStream-Pro-OBS-Nativ`.
3. Натисни **Commit changes**.
4. Перейди в **Actions** і дочекайся збірки.
5. Скачай Windows artifact.
6. Закрий OBS.
7. Замінити DLL або зібрати інсталятор через:

```bat
tools\MAKE_INSTALLER_FROM_ACTIONS_ARTIFACT.bat
```

Готовий інсталятор буде тут:

```text
installer\output\TiHiY_MultiStream_Pro_OBS_Plugin_Setup_v2.2.exe
```
