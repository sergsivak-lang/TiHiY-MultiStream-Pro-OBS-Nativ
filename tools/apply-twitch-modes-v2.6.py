from pathlib import Path

header = Path("src/tihiy-multistream-dock.hpp")
cpp = Path("src/tihiy-multistream-dock.cpp")

h = header.read_text(encoding="utf-8")
h = h.replace("#include <QLabel>\n", "#include <QLabel>\n#include <QComboBox>\n")
h = h.replace("    QCheckBox *twitchSafeCpu_ = nullptr;\n", "    QComboBox *twitchMode_ = nullptr;\n")
header.write_text(h, encoding="utf-8")

s = cpp.read_text(encoding="utf-8")

s = s.replace(
    'twitchDialog_ = makeTargetDialog("Twitch 1080p60", twitch_, "rtmp://live.twitch.tv/app", 1920, 1080, 60, 6000, 160);',
    'twitchDialog_ = makeTargetDialog("Twitch", twitch_, "rtmp://live.twitch.tv/app", 1920, 1080, 60, 7500, 160);\n\n    twitchMode_ = new QComboBox();\n    twitchMode_->addItem("HD 1080p60");\n    twitchMode_->addItem("2K 1440p60");\n    twitchMode_->addItem("2K 1440p60 + Vertical");\n    twitchMode_->setCurrentIndex(0);\n    twitchMode_->setToolTip("Twitch mode. 2K requires OBS 32+ and Twitch Enhanced Broadcasting. Vertical requires Aitum Vertical.");\n    main->addWidget(new QLabel("<b>Twitch mode</b>"));\n    main->addWidget(twitchMode_);'
)

s = s.replace(
    'applyRecommendedButton_->setToolTip("Apply YouTube 2K60 + Twitch 1080p60 recommended preset.");',
    'applyRecommendedButton_->setToolTip("Apply YouTube 2K60 + Twitch HD recommended preset.");'
)

s = s.replace(
'''    twitchSafeCpu_ = new QCheckBox("Twitch safe 1080 fix");
    twitchSafeCpu_->setToolTip("Stable Twitch 1080p mode when OBS canvas is 2560x1440.");
    twitchSafeCpu_->setChecked(true);
    main->addWidget(twitchSafeCpu_);

''', '')

old = '''    const bool twitchSafe = (name == "Twitch" && twitchSafeCpu_ && twitchSafeCpu_->isChecked());
    const char *videoEncoderId = twitchSafe ? VIDEO_ENCODER_ID_X264 : VIDEO_ENCODER_ID_NVENC;
'''
new = '''    int twitchMode = 0;
    if (name == "Twitch" && twitchMode_)
        twitchMode = twitchMode_->currentIndex();

    if (name == "Twitch") {
        if (twitchMode == 1 || twitchMode == 2) {
            ui.width->setValue(2560);
            ui.height->setValue(1440);
            ui.fps->setValue(60);
            ui.videoBitrate->setValue(9000);
            appendLog(twitchMode == 1
                ? "Twitch 2K profile: 2560x1440@60, 9 Mbps. Enhanced Broadcasting must be enabled in OBS."
                : "Twitch 2K + Vertical profile: 2560x1440@60 + 1080x1920 vertical canvas. Enhanced Broadcasting + Aitum Vertical required.");
        } else {
            ui.width->setValue(1920);
            ui.height->setValue(1080);
            ui.fps->setValue(60);
            ui.videoBitrate->setValue(7500);
            appendLog("Twitch HD profile: 1920x1080@60, 7.5 Mbps.");
        }
    }

    const char *videoEncoderId = VIDEO_ENCODER_ID_NVENC;
'''
if old not in s:
    raise SystemExit("encoder block not found")
s = s.replace(old, new)

old = '''    if (twitchSafe) {
        obs_data_set_string(vSettings, "preset", "veryfast");
        appendLog(name + ": Twitch safe 1080 fix enabled, using x264 fallback for scaled 1080p output.");
    } else {
        obs_data_set_string(vSettings, "preset", "p5");
        obs_data_set_string(vSettings, "tuning", "hq");
        obs_data_set_string(vSettings, "multipass", "qres");
        obs_data_set_bool(vSettings, "lookahead", false);
        obs_data_set_bool(vSettings, "psycho_aq", true);
        obs_data_set_int(vSettings, "bframes", 2);
    }
'''
new = '''    obs_data_set_string(vSettings, "preset", "p5");
    obs_data_set_string(vSettings, "tuning", "hq");
    obs_data_set_string(vSettings, "multipass", "qres");
    obs_data_set_bool(vSettings, "lookahead", false);
    obs_data_set_bool(vSettings, "psycho_aq", true);
    obs_data_set_int(vSettings, "bframes", 2);
'''
if old not in s:
    raise SystemExit("encoder settings block not found")
s = s.replace(old, new)

old = '''    handle.output = obs_output_create(OUTPUT_ID, (name + " Output").toUtf8().constData(), nullptr, nullptr);
'''
new = '''    if (name == "Twitch" && twitchMode > 0) {
        if (twitchMode == 2 && !obs_get_module("vertical-canvas")) {
            setTargetState(ui, "Aitum Vertical required", "error");
            appendLog("Twitch 2K + Vertical: Aitum Vertical is not detected. Install Aitum Vertical 1.6.4+.");
            releaseTarget(handle);
            updateGlobalState();
            return false;
        }
        appendLog("Twitch 2K modes require OBS Enhanced Broadcasting (Multitrack Video). The profile is prepared by TiHiY MultiStream Pro; the OBS/Twitch service must provide the multitrack path.");
    }

    handle.output = obs_output_create(OUTPUT_ID, (name + " Output").toUtf8().constData(), nullptr, nullptr);
'''
if old not in s:
    raise SystemExit("output creation block not found")
s = s.replace(old, new)

s = s.replace(
'''    setTargetValues(twitch_, "rtmp://live.twitch.tv/app", 1920, 1080, 60, 6000, 160);
    if (twitchSafeCpu_)
        twitchSafeCpu_->setChecked(true);
    appendLog("Recommended preset applied: YouTube 2K60 + Twitch 1080p60 safe mode.");
''',
'''    setTargetValues(twitch_, "rtmp://live.twitch.tv/app", 1920, 1080, 60, 7500, 160);
    if (twitchMode_)
        twitchMode_->setCurrentIndex(0);
    appendLog("Recommended preset applied: YouTube 2K60 + Twitch HD 1080p60.");
''')

s = s.replace(
'''    if (twitchSafeCpu_)
        s.setValue("twitchSafeCpu", twitchSafeCpu_->isChecked());
''',
'''    if (twitchMode_)
        s.setValue("twitchMode", twitchMode_->currentIndex());
''')

s = s.replace(
'''    if (twitchSafeCpu_)
        twitchSafeCpu_->setChecked(s.value("twitchSafeCpu", true).toBool());
''',
'''    if (twitchMode_)
        twitchMode_->setCurrentIndex(s.value("twitchMode", 0).toInt());
''')

cpp.write_text(s, encoding="utf-8")
print("Twitch mode migration applied")
