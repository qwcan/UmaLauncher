import os
from loguru import logger


def start():
    logger.info("Launching Uma Musume via Steam.")
    os.system("Start steam://rungameid/3224770")