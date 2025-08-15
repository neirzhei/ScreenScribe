import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    VISION_MODEL_REVISION = "2025-06-21"
    VISION_PROMPT = "Describe this screenshot in a short, factual sentence."

    LLM_GPU_LAYERS = int(os.getenv("LLM_GPU_LAYERS", 0))
    LLM_SYSTEM_PROMPT = (
        "Given a factual description of a user's computer screen, make a really short encouraging or witty comment about it in a single sentence."

    )
    LLM_MAX_TOKENS = 30

    MIN_INTERVAL_MINUTES = 1
    MAX_INTERVAL_MINUTES = 5