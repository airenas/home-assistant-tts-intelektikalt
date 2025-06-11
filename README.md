# Intelektika.lt TTS Integration

The Intelektika.lt TTS Integration is a custom component for Home Assistant that provides Lithuanian text-to-speech (TTS) functionality using the REST API.

## Features

- Converts text to speech in Lithuanian.
- Supports multiple voices.

## Installation

1. **Manual Installation**:
   - Download the `custom_components/intelektikalt_tts` folder from this repository.
   - Copy the folder into your Home Assistant `custom_components` directory.

2. **HACS Installation**:
   - Add this repository to HACS as a custom repository.
   - Search for "Intelektika.lt TTS Integration" in HACS and install it.

3. Restart Home Assistant after installation.

## Configuration

1. Go to **Settings** > **Devices & Services** > **Integrations**.
2. Click **Add Integration** and search for "Intelektika.lt TTS".
3. (Optional) Enter your API key and configure the integration. Otherwise, 5000 monthly symbols limit will be applied.

### Example `configuration.yaml` (if required)

```yaml
tts:
  - platform: intelektikalt_tts
    api_key: YOUR_API_KEY # Optional, if you want to use your own API key
    language: lt
    voice: laimis
```

## Supported Voices

The integration supports the following voices:

- Laimis
- Lina
- Astra
- Vytautas

See samples at [Intelektika.lt Voices](https://snekos-sinteze.lt).

## Usage

Once configured, you can use the TTS service in Home Assistant automations or scripts. Example:

```yaml
- action: tts.speak
  target:
    entity_id: tts.intelektika_lt_tts
  data:
    cache: true
    media_player_entity_id: media_player.your_media_player
    message: "Sveiki atvykę į namus!"
    language: lt
    options:
      voice: laimis    
```

## Troubleshooting

- Ensure your API key is valid.
- Check the Home Assistant logs for any errors.
- Verify that your media player supports TTS playback.

## Links

- [Documentation](https://github.com/airenas/home-assistant-tts-intelektikalt)
- [Issue Tracker](https://github.com/airenas/home-assistant-tts-intelektikalt/issues)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

