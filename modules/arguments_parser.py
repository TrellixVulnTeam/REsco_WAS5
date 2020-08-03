from modules.meta import TOOL_NAME, CONFIG_FILE, LOGGER
from shutil import copyfile
import logging
import subprocess
import os
import toml


class REsco(object):
    """ Tool to assess genome quality """

    def __init__(self, config_path="config.toml", monthly_log=True, logging_level=logging.INFO):
        self._config_path = config_path
        self._monthly_log = monthly_log
        self._logging_level = logging_level
    
    def init(self, path = ""):
        """     initializes the project """
        try:
            gt_cmd = "which gt"
            gt_tool_path = subprocess.check_output(gt_cmd.split()).decode().replace("\n", '')
            print(f"gt tools at '{gt_tool_path}'")
        except Exception as e:
            print("ex: ", e)
        return
        data = toml.load(self._config_path)
        data["general"]["GENOME_TOOLS_PATH"] = gt_tool_path

        if path == "":
            path = os.getcwd()
            data["general"]["HOME_DIR"] = path
            print(f"path: {path}")
        else:
            path = os.path.abspath(path)
            data["general"]["HOME_DIR"] = path
            print(f"path: {path}")

        cfg_content = toml.dumps(data)
        
        file = open(self._config_path, "w")
        file.write(cfg_content)
        file.close()

        os.mkdir(os.path.join(path, 'Test'))
        os.mkdir(os.path.join(path, 'Test', 'In'))
        os.mkdir(os.path.join(path, 'Test', 'Config'))

        return
        logger = logging.getLogger(LOGGER)
        logger.setLevel(self._logging_level)

        copyfile(".config_template.toml", path + "/config.toml")

    def run(self, config_path = ""):
        """     starts snakemake """
        if config_path != "":
            self._config_path = config_path
        print("called run")
        cores = 3
        snakemake_cmd = f"snakemake -j {cores} -s Snakefile"
        print(subprocess.Popen(snakemake_cmd.split()))

    def new(self, cmd):
        """     creates config """
        if cmd == "config":
            print("creating config file")
            print(self._config_path)
            logger = logging.getLogger(LOGGER)
            logger.info(f"creating config file 'config.toml'")
            copyfile(".config_template.toml", "config.toml")

    def create_config_from_folder(self, path):

        output = ""

        for file in os.listdir(path):
            name = file[:file.find(".")]
            #path = file.path
            dir = os.path.realpath(path)
            dir = os.path.join(dir, file)

            output += "[[genome_assemblies]]\n"
            output += f'fasta = "{dir}\n'
            output += f'genome_id = "{name}"\n'
            output += f'species = "{name}"\n'
            output += f'genome_size = {os.path.getsize(dir)}\n'
            output += "\n"

        print(f"'{output}'")

        