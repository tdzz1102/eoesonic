import configparser
from pathlib import Path


config = configparser.ConfigParser()
config_ini_path = Path(__file__).parent.parent / 'config.ini'
config.read(str(config_ini_path))

