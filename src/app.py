import time
import random
import logging
import gc

from .config import Config
from .vision import Vision
from .language import Language
from .speech import Speech

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - (%(module)s) - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def main_cycle():

    logging.info("-------Starting-------")

    vision_module = Vision()
    caption = vision_module.get_caption()
    del vision_module
    gc.collect()

    if not caption:
        logging.warning("Could not get a caption. Ending.")
        return

    language_module = Language()
    response = language_module.get_response(caption)
    del language_module
    gc.collect()

    if not response:
        logging.warning("Could not get a response. Ending.")
        return

    speech_module = Speech()
    speech_module.speak(response)
    del speech_module
    gc.collect()

    logging.info("-------Finished-------")

def main():

    logging.info("Waiting for first interval")
    while True:
        try:
            sleep_duration_minutes = random.uniform(
                Config.MIN_INTERVAL_MINUTES,
                Config.MAX_INTERVAL_MINUTES
            )
            sleep_duration_seconds = sleep_duration_minutes * 60
            logging.info(f"Next check in {sleep_duration_minutes} minutes.")
            time.sleep(sleep_duration_seconds)

            main_cycle()

        except KeyboardInterrupt:
            logging.info("-------Stopped by user-------")
            break
        except Exception as e:
            logging.critical(f"Error occurred in the main loop: {e}", exc_info=True)
            time.sleep(60)

if __name__ == "__main__":
    main()
