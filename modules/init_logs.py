from datetime import datetime
import time
import logging
import os

from modules.meta import LOGGER, LOG_FILE_SUFFIX



def setup_logger(log_create_monthly_dir : bool, level = logging.INFO):
    logger = logging.getLogger(LOGGER)

    date = datetime.now()
    year = date.year
    month = date.month
    day = date.day

    current_dir = os.path.dirname(os.path.realpath(__file__))

    if not os.path.exists("logs"):
        os.mkdir("logs")

    # creates dir: Year/Month/day_tool.log
    if log_create_monthly_dir:
        log_file_path = os.path.join(current_dir, "logs", str(year), str(month),
                                    str(day) + "_"+ LOG_FILE_SUFFIX)
        os.makedirs(os.path.join(current_dir, "logs", str(year), str(month)), exist_ok=True)
    else:
        log_file_path = os.path.join(current_dir, "logs",
                                     str(year) + "-" + str(month) + "-" + str(day) + "-" +
                                     date.strftime("%H%M:%S") + "." + LOG_FILE_SUFFIX)

    logging.basicConfig(filename=log_file_path, filemode='a',
                        level=logging.ERROR,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    ch = logging.StreamHandler()

    logger.setLevel(level)

    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(ch)

    logger.info(f"log files at {os.path.join(current_dir, 'logs')}")

