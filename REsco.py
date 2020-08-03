import logging
import os
import os.path
import subprocess
import fire

from modules.config_file import ConfigFile
from modules.meta import TOOL_NAME, TOOL_VERSION, LOG_FILE_SUFFIX, LOGGER, CONFIG_FILE
from modules import tests, meta, arguments_parser, init_logs


def main():
    #logger = logging.getLogger(LOGGER)

    args = arguments_parser.REsco()
    fire.Fire(args)

    #init_logs.setup_logger(args._monthly_log)
    #logger.info(f"Tool Version: {TOOL_VERSION}")
    #print(f"executable at {os.path.dirname(os.path.realpath(__file__))}") # where main.py is
    #print(f"executed from {os.getcwd()}") # current working directory, where was main.py called from


if __name__ == "__main__":
    main()

