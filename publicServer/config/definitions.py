import configparser
import os
from publicServer.config.constants import CONFIG_FILE_NAME

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))
CONFIG_DIR = os.path.join(ROOT_DIR, "config")
config = configparser.ConfigParser()
config.read(CONFIG_DIR + CONFIG_FILE_NAME)

API_KEY = config.get("API", "API_KEY")
SECRET_KEY = config.get("SECRETS", "SECRET_KEY")
EMAIL = config.get("EMAIL", "EMAIL")
EMAIL_PASSWORD = config.get("EMAIL", "EMAIL_PASSWORD")
SMTP_SERVER = config.get("EMAIL", "SMTP_SERVER")
KEY_URL = "apikey=" + API_KEY
