from llama_cpp import Llama
import logging
import sys
from .config import Config

class Language:
    def __init__(self):
        self.llm = None
        try:
            repo_id = "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF"
            filename = "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
            logging.info(f"Offloading {Config.LLM_GPU_LAYERS} layers to GPU.")
            self.llm = Llama.from_pretrained(
                repo_id=repo_id,
                filename=filename,
                n_gpu_layers=Config.LLM_GPU_LAYERS,
                n_ctx=2048,
                verbose=False,
                chat_format="chatml"
            )
            logging.info("Language model loaded")
        except Exception as e:
            logging.error(f"Failed to load language model: {e}", exc_info=True)
            sys.exit(1)

    def get_response(self, caption: str) -> str | None:
        """Generates response based on the caption."""

        if not self.llm or not caption:
            return None

        messages = [
            {"role": "system", "content": Config.LLM_SYSTEM_PROMPT},
            {"role": "user", "content": caption},
        ]

        try:
            logging.info("Generating response...")
            outputs = self.llm.create_chat_completion(
                messages=messages,
                max_tokens=Config.LLM_MAX_TOKENS,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
            )
            response = outputs["choices"][0]["message"]["content"].strip()
            logging.info(f"Generated response: '{response}'")
            return response
        except Exception as e:
            logging.error(f"Failed to generate response: {e}", exc_info=True)
            return None