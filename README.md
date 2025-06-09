# IntelektikaLT TTS Integration

The IntelektikaLT TTS Integration is a custom component for Home Assistant that provides Lithuanian text-to-speech (TTS) functionality using the IntelektikaLT REST API.

## Features

- Converts text to speech in Lithuanian.
- Supports multiple voices.
- Integrates seamlessly with Home Assistant's TTS platform.

## Installation

1. **Manual Installation**:
   - Download the `custom_components/intelektikalt_tts` folder from this repository.
   - Copy the folder into your Home Assistant `custom_components` directory.

2. **HACS Installation**:
   - Add this repository to HACS as a custom repository.
   - Search for "IntelektikaLT TTS Integration" in HACS and install it.

3. Restart Home Assistant after installation.

## Configuration

1. Go to **Settings** > **Devices & Services** > **Integrations**.
2. Click **Add Integration** and search for "IntelektikaLT TTS".
3. Enter your API key and configure the integration.

### Example `configuration.yaml` (if required)

```yaml
tts:
  - platform: intelektikalt_tts
    api_key: YOUR_API_KEY
    language: lt
    voice: laimis
```

## Supported Voices

The integration supports the following voices:

- Laimis
- Lina
- Astra
- Vytautas

## Usage

Once configured, you can use the TTS service in Home Assistant automations or scripts. Example:

```yaml
service: tts.intelektikalt_tts_say
data:
  entity_id: media_player.your_media_player
  message: "Sveiki atvykę į namus!"
  options:
    voice: lina
```

## Troubleshooting

- Ensure your API key is valid.
- Check the Home Assistant logs for any errors.
- Verify that your media player supports TTS playback.

## Links

- [Documentation](https://github.com/airenas/home-assistant-tts-intelektikalt)
- [Issue Tracker](https://github.com/airenas/home-assistant-tts-intelektikalt/issues)

## License
