import sys
import logging
import io
import wave
import simpleaudio as sa
from piper import PiperVoice
from huggingface_hub import hf_hub_download

class Speech:
    def __init__(self):
        self.voice = None
        try:
            repo_id = "rhasspy/piper-voices"
            model_path_in_repo = "en/en_US/joe/medium/en_US-joe-medium.onnx"
            config_path_in_repo = "en/en_US/joe/medium/en_US-joe-medium.onnx.json"

            model_path = hf_hub_download(repo_id=repo_id, filename=model_path_in_repo)
            config_path = hf_hub_download(repo_id=repo_id, filename=config_path_in_repo)

            self.voice = PiperVoice.load(model_path, config_path=config_path)
            logging.info("Speech model loaded")
        except Exception as e:
            logging.error(f"Failed to load speech model: {e}", exc_info=True)
            sys.exit(1)

    def speak(self, text: str):
        """Synthesizes a WAV file in memory and plays it"""
        if not self.voice or not text:
            logging.warning("Speech module received no voice or text")
            return

        try:
            logging.info(f"Synthesizing speech for: '{text}'")

            wav_buffer = io.BytesIO()
            with wave.open(wav_buffer, "wb") as wav_writer:
                self.voice.synthesize_wav(text, wav_writer)

            wav_buffer.seek(0)

            with wave.open(wav_buffer, 'rb') as wav_reader:
                wave_obj = sa.WaveObject.from_wave_read(wav_reader)

                logging.info("Playing audio...")
                play_obj = wave_obj.play()
                play_obj.wait_done()
                logging.info("Playback ended")

        except Exception as e:
            logging.error(f"Failed to synthesize or play speech: {e}", exc_info=True)