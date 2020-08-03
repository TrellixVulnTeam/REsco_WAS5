


class Types:
    STRING = 'str'
    INTEGER = 'int'
    FLOAT = 'float'
    ARRAY = 'arr'
    BOOL = 'bool'
    RANGE = 'range'
    UNDEFINED = 'undefined'
    NO_ARGS = 'no_args'


def cast(text : str, type : str):
    if type == Types.INTEGER:
        return int(text)
    elif type == Types.FLOAT:
        return float(text)
    elif type == Types.ARRAY:
        return (text)
    elif type == Types.BOOL:
        return bool(text)
    elif type == Types.RANGE:
        return int(text)
    elif type == Types.UNDEFINED:
        return text
    elif type == Types.NO_ARGS:
        return text
    else:
        return text


def get_type(text : str):
    if text == 'undefined':
        return Types.UNDEFINED

    if text == 'NO_ARGS':
        return Types.NO_ARGS

    if is_range(text):
        return Types.RANGE

    if is_array(text):
        return Types.ARRAY

    if is_bool(text):
        return Types.BOOL

    if is_float(text):
        return Types.FLOAT

    if is_integer(text):
        return Types.INTEGER

    return Types.STRING


def is_range(text : str):
    if text.lstrip().rstrip().find(' ') == -1:
        return False

    if is_float(text[:text.find(' ')]) or is_integer(text[:text.find(' ')]) and \
        is_float(text[text.find(' ')+1:]) or is_integer(text[text.find(' ')+1:]):
        return True

    return False


def is_array(text : str):
    if text.lstrip(' ').startswith('[') and text.rstrip(' ').endswith(']'):
        return True
    return False


def is_integer(text : str):
    try:
        if is_float(text.lstrip('-').lstrip('+')):
            return False
        int(text.lstrip('-').lstrip('+'))
        return True
    except ValueError:
        return False


def is_float(text : str):
    try:
        if text.find('.') == -1:
            return False
        float(text)
        return True
    except ValueError:
        return False


def is_bool(text : str):
    if text.lower() in ['y', 'yes', 'true', 'n', 'no', 'false']:
        return True
    return False