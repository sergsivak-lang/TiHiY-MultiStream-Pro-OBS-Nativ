#define MyAppName "TiHiY MultiStream Pro OBS Plugin"
#define MyAppVersion "2.5"
#define MyAppPublisher "TiHiY-DED"

[Setup]
AppId={{A7E4F94D-7F3A-4C5E-9B2A-000TIHIYMSP}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName=F:\OOBS\obs-studio
DisableProgramGroupPage=yes
OutputDir=output
OutputBaseFilename=TiHiY_MultiStream_Pro_OBS_Plugin_Setup_v2.5_NO_AUTOSTART
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
UninstallDisplayName={#MyAppName}

[Languages]
Name: "ukrainian"; MessagesFile: "compiler:Languages\Ukrainian.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Створити ярлик OBS на робочому столі"; GroupDescription: "Додатково:"; Flags: unchecked

[Files]
Source: "payload\obs-plugins\64bit\tihiy-multistream-pro.dll"; DestDir: "{app}\obs-plugins\64bit"; Flags: ignoreversion
Source: "payload\data\obs-plugins\tihiy-multistream-pro\*"; DestDir: "{app}\data\obs-plugins\tihiy-multistream-pro"; Flags: ignoreversion recursesubdirs createallsubdirs skipifsourcedoesntexist

[Icons]
Name: "{autodesktop}\OBS Studio"; Filename: "{app}\bin\64bit\obs64.exe"; Tasks: desktopicon

[UninstallDelete]
Type: files; Name: "{app}\obs-plugins\64bit\tihiy-multistream-pro.dll"
