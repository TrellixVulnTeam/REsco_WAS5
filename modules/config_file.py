import toml
import logging
from shutil import copyfile

from .meta import LOGGER
from .help_ouput_fetcher import load_arguments, CLITools
from . import type_check


"""
- creates, saves and loads config file
- has prioerty list which lists the listed args first in the toml file
- has remove_list which remove the args (e.g. help) from the listed args
"""

logger = logging.getLogger(LOGGER)

TOOLS = []


TOOLS.append(CLITools("ltrharvest", "gt ltrharvest -help"))
TOOLS.append(CLITools("suffixerator", "gt suffixerator -help"))

class ConfigFile:
    priority_list = [
        'index',
        'minlenltr',
    ]

    remove_list = [
        'help',
        'help+',
    ]

    config_genomes = []
    config_params = []

    def create_from_copy(self):
        global logger
        logger.info(f"creating config file 'config.toml'")
        copyfile(".config_template.toml", "config.toml")

    def create(self, path):
        global logger
        logger.info(f"create config file: {path}")

        # get the tools
        arg_list = dict()
        for i in range(len(TOOLS)):
            arg_list[TOOLS[i].name] = load_arguments(TOOLS[i].command) # returns [] with 'name', 'description', 'default'

        # read the tools output into string
        # with format key = value # comment
        config_text = ""
        for tool_name in arg_list.keys():
            args = arg_list[tool_name]
            #tools[tool_name] = dict()
            config_text += tool_name + "\n"
            for arg in args:
                config_line = arg.name.lstrip("-") + " = \"" + arg.default + "\""
                config_text += config_line.ljust(24, ' ') + "# " + arg.description.replace("\n", "").replace(" " * 12, " ")
                config_text += "\n"
                #tools[tool_name][arg.name.lstrip('-')] = type_check.cast(arg.default, type_check.get_type(arg.default))

        # write to file
        file = open("tools_output.txt", "w")
        file.write(config_text)
        file.close()
        return

        data = {}
        general = data["GENERAL"] = dict()

        input_genomes = data["input_genome_assemblies"] = []
        input_genomes.append(dict())
        example_genome = input_genomes[0]

        input_params = data["ltr_harvest_parameters"] = []
        input_params.append(dict())
        example_param = input_params[0]

        tools = data["TOOLS"] = dict()

        ### GENERAL
        general["GENOME_TOOLS_PATH"] = ""
        general["HOME_DIR"] = ""
        general["delete_existing_species_home"] = True

        ### Example input genome
        example_genome["genome_id"] = ""
        example_genome["fasta"] = ""
        example_genome["species"] = ""
        example_genome["genome_size"] = 0

        ### Example input params
        example_param["genome_id"] = ""

        ###  TOOLS

        for c in arg_list.keys():
            args = arg_list[c]
            tools[c] = dict()
            for arg in args:
                #print(arg.default, type_check.get_type(arg.default), arg.name.lstrip('-'))
                tools[c][arg.name.lstrip('-')] = type_check.cast(arg.default, type_check.get_type(arg.default))

        config_text = pytoml.dumps(data, False)

        # write to file
        file = open(path, "w")
        file.write(config_text)
        file.close()

    def load(self, path):
        global logger
        logger.info(f"load config file: {path}")
        data = toml.load(path)

        tools = data["general"]

        return data

        #print(data["input"][0]["genomes_path"])

        cmdCommands = []

        for tool in tools:
            cmdStr = "gt " + tool + " "
            for arg in data["tools"][tool]:
                if data["tools"][tool][arg] == 'undefined':
                    continue
                elif data["tools"][tool][arg] == 'NO_ARGS':
                    cmdStr += arg + " "
                else:
                    cmdStr += arg + " " + data["tools"][tool][arg] + " "

            cmdCommands.append(cmdStr)

    def get_config_params(self):
        return

    def get_config_genomes(self):
        return

    def save(self, path):
        print(f"save config file: {path}")