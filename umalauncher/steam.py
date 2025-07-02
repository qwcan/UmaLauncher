import os
from loguru import logger


def start():
    logger.info("Launching Uma Musume via Steam.")
    os.system("steam://rungameid/3224770")