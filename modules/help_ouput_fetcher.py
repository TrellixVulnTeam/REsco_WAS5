import subprocess


class CLICommand:
    name: str = ""
    description: str = ""
    default = "NO_ARGS"
    type = type("")


class CLITools:
    name = ""
    command = ""

    def __init__(self, _name, _command):
        self.name = _name
        self.command = _command


# feteches the command line input-options for a command
# 1 find first '\n-arg'
# 2 loop until
def fetch_parameters(cli_output: str):
    parameters = []

    token = '\n-'

    # crop to the arguments parts
    from_position = cli_output.find("\n\n-")
    to_position = cli_output.find("\n\n", from_position + 3)
    cli_output = cli_output[from_position:to_position]

    # first token needs to be \n\n- because of empty line before
    find_idx = cli_output.find('\n\n-', 0)+3

    # loop through args and gather name+description
    while (find_idx != -1):
        param_name: str = cli_output[find_idx:cli_output.find(' ', find_idx)].lstrip().rstrip()

        if cli_output.find(token, find_idx + 1) != -1:
            param_description: str = cli_output[cli_output.find(' ', find_idx):cli_output.find(token, find_idx + 1)]
        else:
            param_description: str = cli_output[cli_output.find(' ', find_idx):]

        command = CLICommand()

        command.name = param_name.lstrip()
        command.description = param_description.lstrip()

        if param_description.find("default:") != -1:
            defStr = "default:"
            param_default: str = param_description[param_description.find(defStr) + len(defStr) + 1:]
            command.default = param_default

            command.type = type(command.default)

        # check for single newline, which means the command ends
        find_idx = cli_output.find(token, find_idx + 1)

        #print("Found: ", command.name)

        parameters.append(command)

    #print("Found ", len(parameters), " args.")
    #print('')

    return parameters  # parameters[i] has 'name' and 'description'


# returns array : 'name', 'description'
def load_arguments(command: str):
    # output = subprocess.check_output(['man', 'gt'])
    help_output = subprocess.run(command.split(), stdout=subprocess.PIPE).stdout.decode('utf-8')
    return fetch_parameters(help_output)