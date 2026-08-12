$ErrorActionPreference = 'Stop'

$path = 'src/tihiy-multistream-dock.cpp'
$text = Get-Content -Raw -LiteralPath $path

$text = $text.Replace('twitchMode_->addItem("2K 1440p60");', 'twitchMode_->addItem("2K 1440p60 — Enhanced Broadcasting");')
$text = $text.Replace('twitchMode_->addItem("2K 1440p60 + Vertical");', 'twitchMode_->addItem("2K 1440p60 + Vertical — Dual Format");')

$marker = 'bool TihiyMultistreamDock::startTwitchEnhanced()'
if (-not $text.Contains($marker)) { throw 'startTwitchEnhanced marker not found.' }

$helper = @'
static bool prepareTwitch2KVideo(QString &error)
{
    obs_video_info ovi{};
    if (!obs_get_video_info(&ovi)) {
        error = "Unable to read current OBS video configuration.";
        return false;
    }

    if (ovi.base_width >= 2560 && ovi.base_height >= 1440 &&
        ovi.output_width >= 2560 && ovi.output_height >= 1440 &&
        ovi.fps_num == 60 && ovi.fps_den == 1) {
        return true;
    }

    if (obs_frontend_streaming_active()) {
        error = "OBS streaming is already active; stop the current stream before switching video mode.";
        return false;
    }

    ovi.graphics_module = "libobs-d3d11";
    ovi.fps_num = 60;
    ovi.fps_den = 1;
    ovi.base_width = 2560;
    ovi.base_height = 1440;
    ovi.output_width = 2560;
    ovi.output_height = 1440;
    ovi.adapter = 0;

    const int result = obs_reset_video(&ovi);
    if (result != OBS_VIDEO_SUCCESS) {
        error = QString("OBS could not switch to 2560x1440@60 (code %1).").arg(result);
        return false;
    }

    config_t *profile = obs_frontend_get_profile_config();
    if (profile) {
        config_set_uint(profile, "Video", "BaseCX", 2560);
        config_set_uint(profile, "Video", "BaseCY", 1440);
        config_set_uint(profile, "Video", "OutputCX", 2560);
        config_set_uint(profile, "Video", "OutputCY", 1440);
        config_set_uint(profile, "Video", "FPSInt", 60);
        config_set_uint(profile, "Video", "FPSNum", 60);
        config_set_uint(profile, "Video", "FPSDen", 1);
        config_save(profile);
    }

    return true;
}

'@

if (-not $text.Contains('static bool prepareTwitch2KVideo')) {
    $text = $text.Replace($marker, $helper + $marker)
}

$oldEnsure = @'
    const QString obsVersion = QString::fromUtf8(obs_get_version_string());
    if (obs_get_version() < 0x2000000) {
        setTargetState(twitch_, "OBS 32+ REQUIRED", "error");
        appendLog("Twitch 2K: OBS Studio 32.0+ is required. Current version: " + obsVersion);
        return false;
    }
'@
$newEnsure = @'
    const QString obsVersion = QString::fromUtf8(obs_get_version_string());
    const uint32_t obsVersionValue = obs_get_version();
    if (obsVersionValue < ((32u << 24) | (0u << 16) | 0u)) {
        setTargetState(twitch_, "OBS 32+ REQUIRED", "error");
        appendLog("Twitch 2K: OBS Studio 32.0+ is required. Current version: " + obsVersion);
        return false;
    }

    if (youtubeOut_.output || customOut_.output) {
        setTargetState(twitch_, "STOP OTHER OUTPUTS FIRST", "error");
        appendLog("Twitch 2K: stop YouTube/Custom first so OBS video can switch safely to 2560x1440.");
        return false;
    }

    QString videoError;
    if (!prepareTwitch2KVideo(videoError)) {
        setTargetState(twitch_, "2K VIDEO SETUP FAILED", "error");
        appendLog("Twitch 2K: " + videoError);
        return false;
    }
'@
if (-not $text.Contains($oldEnsure)) { throw 'OBS version block not found.' }
$text = $text.Replace($oldEnsure, $newEnsure)

$oldService = @'
    obs_data_t *settings = obs_data_create();
    obs_data_set_string(settings, "service", "Twitch");
    obs_data_set_string(settings, "server", twitch_.server->text().toUtf8().constData());
    obs_data_set_string(settings, "key", twitch_.key->text().toUtf8().constData());
    obs_data_set_bool(settings, "using_custom_server", false);
    obs_data_set_bool(settings, "bwtest", false);
    obs_service_t *service = obs_service_create(SERVICE_ID, "TiHiY Twitch Enhanced", settings, nullptr);
    obs_data_release(settings);

    if (!service) {
        setTargetState(twitch_, "TWITCH SERVICE FAILED", "error");
        appendLog("Twitch 2K: failed to create native Twitch service.");
        return false;
    }

    obs_frontend_set_streaming_service(service);
    obs_frontend_save_streaming_service();
    obs_service_release(service);
'@
$newService = @'
    obs_service_t *currentService = obs_frontend_get_streaming_service();
    obs_service_t *service = nullptr;

    if (currentService && QString::fromUtf8(obs_service_get_type(currentService)) == SERVICE_ID) {
        service = obs_service_get_ref(currentService);
        obs_data_t *settings = obs_service_get_settings(service);
        obs_data_set_string(settings, "service", "Twitch");
        obs_data_set_string(settings, "server", twitch_.server->text().toUtf8().constData());
        obs_data_set_string(settings, "key", twitch_.key->text().toUtf8().constData());
        obs_data_set_bool(settings, "using_custom_server", false);
        obs_data_set_bool(settings, "bwtest", false);
        obs_service_update(service, settings);
        obs_data_release(settings);
    } else {
        obs_data_t *settings = obs_data_create();
        obs_data_set_string(settings, "service", "Twitch");
        obs_data_set_string(settings, "server", twitch_.server->text().toUtf8().constData());
        obs_data_set_string(settings, "key", twitch_.key->text().toUtf8().constData());
        obs_data_set_bool(settings, "using_custom_server", false);
        obs_data_set_bool(settings, "bwtest", false);
        service = obs_service_create(SERVICE_ID, "TiHiY Twitch Enhanced", settings, nullptr);
        obs_data_release(settings);
    }

    if (!service) {
        setTargetState(twitch_, "TWITCH SERVICE FAILED", "error");
        appendLog("Twitch 2K: failed to access/create the Twitch service.");
        return false;
    }

    obs_frontend_set_streaming_service(service);
    obs_frontend_save_streaming_service();
    obs_service_release(service);
'@
if (-not $text.Contains($oldService)) { throw 'Twitch service block not found.' }
$text = $text.Replace($oldService, $newService)

$oldStartAll = @'
    bool startedAny = false;
    if (youtube_.enabled->isChecked()) startedAny = startTarget("YouTube", youtube_, youtubeOut_) || startedAny;
    if (twitch_.enabled->isChecked()) {
        const int mode = twitchMode_ ? twitchMode_->currentIndex() : 0;
        if (mode > 0) startedAny = startTwitchEnhanced() || startedAny;
        else startedAny = startTarget("Twitch", twitch_, twitchOut_) || startedAny;
    }
    if (custom_.enabled->isChecked()) startedAny = startTarget("Custom", custom_, customOut_) || startedAny;
'@
$newStartAll = @'
    bool startedAny = false;
    const int twitchMode = twitchMode_ ? twitchMode_->currentIndex() : 0;

    // Enhanced Broadcasting may need to reset OBS video to 2560x1440 before any output is active.
    if (twitch_.enabled->isChecked() && twitchMode > 0)
        startedAny = startTwitchEnhanced() || startedAny;

    if (youtube_.enabled->isChecked()) startedAny = startTarget("YouTube", youtube_, youtubeOut_) || startedAny;

    if (twitch_.enabled->isChecked() && twitchMode == 0)
        startedAny = startTarget("Twitch", twitch_, twitchOut_) || startedAny;

    if (custom_.enabled->isChecked()) startedAny = startTarget("Custom", custom_, customOut_) || startedAny;
'@
if (-not $text.Contains($oldStartAll)) { throw 'Start All block not found.' }
$text = $text.Replace($oldStartAll, $newStartAll)

Set-Content -LiteralPath $path -Value $text -Encoding UTF8
Write-Host 'Patched Twitch v2.6 runtime support.'
