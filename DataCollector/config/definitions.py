import configparser
import os
from DataCollector.config.constants import CONFIG_FILE_NAME

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
CONFIG_DIR = os.path.join(ROOT_DIR, "config")
config = configparser.ConfigParser()
config.read(CONFIG_DIR + CONFIG_FILE_NAME)

API_KEY = config.get("API", "API_KEY")
KEY_URL = "apikey=" + API_KEY
