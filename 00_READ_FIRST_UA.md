# TiHiY MultiStream Pro v2.3 — INSTALLER AUTO BUILD

Це overlay для правильного репозиторію:

`sergsivak-lang/TiHiY-MultiStream-Pro-OBS-Nativ`

## Що нового

- Без Rutony.
- Без автовідкриття чатів.
- Є активні статуси кнопок Start / LIVE / FAILED.
- Додано GitHub Actions workflow, який після успішної збірки DLL автоматично робить `Setup.exe`.

## Як заливати

1. Розпакувати архів v2.3.
2. Відкрити репозиторій `TiHiY-MultiStream-Pro-OBS-Nativ`.
3. `Add file → Upload files`.
4. Завантажити весь вміст розпакованої папки, не саму папку і не ZIP.
5. `Commit changes`.

## Що буде в Actions

Після звичайної збірки DLL з’явиться ще один workflow:

`Build TiHiY Installer v2.3`

Він створить artifact:

`TiHiY-MultiStream-Pro-Setup-v2.3`

Усередині буде готовий інсталятор:

`TiHiY_MultiStream_Pro_OBS_Plugin_Setup_v2.3.exe`

## Встановлення

Запустити Setup.exe, шлях OBS за замовчуванням:

`F:\OOBS\obs-studio`

Інсталятор копіює:

- `tihiy-multistream-pro.dll` → `obs-plugins\64bit`
- `data\locale` → `data\obs-plugins\tihiy-multistream-pro`

Ключі та налаштування OBS не видаляються.
