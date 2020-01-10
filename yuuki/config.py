from argparse import Namespace
from configparser import ConfigParser

try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources


def _parse_config(config_loc: tuple = ('yuuki', 'yuuki.conf')) -> Namespace:
    """
    Parse and return a config file as a dictionary
    :arg config_loc: tuple path of the config file, default ('yuuki', 'yuuki.conf')
    """
    config_file = resources.open_text(*config_loc)
    parser = ConfigParser()
    parser.read_file(config_file)
    return Namespace(**{s: Namespace(**dict(parser.items(s))) for s in parser.sections()})


# Console colors. No need to pollute yuuki.conf with these.
_GREEN = '\033[32m'
_BLUE = '\033[34m'
_console = Namespace(
    BOLD='\033[1m',
    _GREEN=_GREEN,
    _BLUE=_BLUE,
    END='\033[0m',
    DEFAULT=_GREEN,
    COMMAND=_GREEN,
    RESPONSE=_BLUE
)


class Config:
    """
    Config shared by both client and actuator, populated by yuuki.conf.
    """
    defaults = None
    Console = _console


# Populate Config class above with data from config file.
for k, v in vars(_parse_config()).items():
    setattr(Config, k, v)

# Turn off coloring if needed.
if getattr(Config.defaults, 'console_coloring', 'Off') != 'On':
    Config.Console = Namespace(**{k: '' for k in vars(Config.Console)})
