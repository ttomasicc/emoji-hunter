__author__ = "Tin Tomašić"

from configparser import ConfigParser


def get_configuration() -> ConfigParser:
    """ Returns default ConfigParser

    Returns
    -------
    ConfigParser - default ConfigParser
    """
    configuration = ConfigParser()
    configuration.read("config/config.ini", "utf-8")
    return configuration
