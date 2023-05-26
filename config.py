import os

from dotenv import load_dotenv

load_dotenv()

AUTH_URL = os.environ.get("AUTH_URL")
URL_VACATION_SERVICE = os.environ.get("URL_VACATION_SERVICE")

PATH_VACATION = os.environ.get("PATH_VACATION")
