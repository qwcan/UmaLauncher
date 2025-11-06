import os
from loguru import logger


def start():
    logger.info("Launching Uma Musume via Steam.")
    if 'IS_JP_STEAM' in os.environ:
        # JP
        os.system("Start steam://rungameid/3564400")
    else:
        # Global
        os.system("Start steam://rungameid/3224770")