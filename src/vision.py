import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
import mss
import sys
import logging
from .config import Config

class Vision:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = "cpu"

        try:
            model_id = "vikhyatk/moondream2"
            logging.info(f"Loading vision model")
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id,
                trust_remote_code=True,
                revision=Config.VISION_MODEL_REVISION
            ).to(self.device)
            self.model.eval()
            logging.info("Vision model loaded")
        except Exception as e:
            logging.error(f"Failed to load vision model: {e}", exc_info=True)
            sys.exit(1)

    def _capture_screenshot(self) -> Image.Image | None:
        try:
            with mss.mss() as sct:
                monitor_index = 1
                mon = sct.monitors[monitor_index]
                sct_img = sct.grab(mon)
                img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
                logging.info(f"Screenshot captured")
                return img
        except Exception as e:
            logging.error(f"Failed to capture screenshot: {e}", exc_info=True)
            return None

    def get_caption(self) -> str | None:
        image = self._capture_screenshot()
        if not image or self.model is None or self.tokenizer is None:
            return None

        try:
            logging.info("Generating image caption...")
            enc_image = self.model.encode_image(image)
            caption = self.model.answer_question(
                enc_image,
                Config.VISION_PROMPT,
                tokenizer=self.tokenizer
            )
            logging.info(f"Generated caption: '{caption}'")
            return caption
        except Exception as e:
            logging.error(f"Failed to generate caption: {e}", exc_info=True)
            return None