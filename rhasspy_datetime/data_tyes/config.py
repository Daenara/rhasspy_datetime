import configparser
import logging
import os
from pathlib import Path

import pytz

from rhasspy_datetime.data_tyes.error import ConfigError

log = logging.getLogger(__name__)
config_path = os.path.join(str(Path(__file__).parent.parent.parent), 'config.ini')

config_sections = {
    "General": "__parse_section_general"
}


class Config:

    def __init__(self, current_config_path):
        log.info("Loading config")

        self.timezone = None
        self.__locale = None
        self.exact_time = None
        self.use_24_hour_system = None

        self.__config_parser = configparser.ConfigParser(allow_no_value=True)
        self.__config_parser.read(current_config_path)

        for section, function_string in config_sections.items():
            getattr(self, "_Config" + function_string)(self.__config_parser[section])

        log.info("Config Loaded")

    def __parse_section_general(self, section):
        if section is None:
            log.error(f"Required section {section} is missing. Please refer to 'config.default' for an example config.")

        self.locale = self.__get_option_with_default_value(section, "locale", "german")
        self.timezone = pytz.timezone(self.__get_option_with_default_value(section, "timezone", "Europe/Berlin"))
        self.exact_time = self.__get_option_with_default_value(section, "exact_time", False, "bool")
        self.use_24_hour_system = self.__get_option_with_default_value(section, "use_24_hour_system", False, "bool")

    def get_external_section(self, section_name):
        if self.__config_parser.has_section(section_name):
            return self.__config_parser[section_name]
        else:
            log.error(f"The section {section_name} is missing but required.")

    @property
    def locale(self):
        return self.__locale

    @locale.setter
    def locale(self, val):
        try:
            self.__locale = __import__("rhasspy_datetime.languages." + val, fromlist=[''])
        except ImportError:
            raise ConfigError("No locale found", "There is no module in the locale folder that matches the locale name in your config.")

    @staticmethod
    def __get_option_with_default_value(section: configparser.SectionProxy, option, default_value, data_type: str = ""):
        if section is not None and option in section:
            try:
                if data_type == "bool":
                    temp = section.getboolean(option)
                elif data_type == "int":
                    temp = section.getint(option)
                elif data_type == "float":
                    temp = section.getfloat(option)
                else:
                    temp = section.get(option)
                if option is None:
                    log.warning(f"Setting '{option}' is present but has no value. Please refer to 'config.default' for an example config.")
                    return default_value
                else:
                    return temp
            except ValueError:
                return default_value
        log.error(f"Setting '{option}' is missing from config. Please refer to 'config.default' for an example config.")
        return default_value


__config = None


def get_config():
    global __config
    global config_path
    if __config is None:
        rhasspy_datetime_path = str(Path(__file__).parent.parent.parent)
        home_path = os.path.join(os.path.expanduser("~"), ".config", "rhasspy_datetime")
        config_names = ["rhasspy_datetime_config.ini", "config.ini", "rhasspy_datetime.ini"]
        if os.path.exists(config_path):
            __config = Config(config_path)
        else:
            log.warning(f"Config not found at '{config_path}'. Searching elsewhere.")
            for loc in rhasspy_datetime_path, home_path:
                for config_name in config_names:
                    tmp_config_path = os.path.join(loc, config_name)
                    if os.path.exists(tmp_config_path):
                        config_path = tmp_config_path
                        __config = Config(config_path)
        if __config is None:
            message = f"No config file found in '{rhasspy_datetime_path}' or '{home_path}'. Please copy config.default into one of those paths and rename it to one of {str(config_names)}"
            raise ConfigError("No config found", message)
    return __config


def set_config_path(new_config_path: str):
    global config_path, __config
    if os.path.exists(new_config_path):
        config_path = new_config_path
        __config = None
    else:
        log.warning(f"Config at {new_config_path} not found.")
