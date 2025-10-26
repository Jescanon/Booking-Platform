import os
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR.parent
ENV_PATH = SRC_DIR / ".env"

load_dotenv(dotenv_path=str(ENV_PATH))

infos = dict(os.environ)

class Config:
    def __init__(self, **args):
        self.info = dict()

        inf = ["ENGINE",
               "USER",
               "PASSWORD",
               "BASE_NAME",
               "DOMAIN",
               "BOT_TOKEN",]

        for key in args:
            if key in inf:
                self.info.update({key: args[key]})

    def get_engine_db(self):
        return f"{self.info['ENGINE']}://{self.info['USER']}:{self.info['PASSWORD']}@{self.info['DOMAIN']}/{self.info['BASE_NAME']}"



configs = Config(**infos)

SECRET_KEY = infos["SECRET_KEY"]
ALGORITHM = infos["ALGORITHM"]
TOKEN = infos["BOT_TOKEN"]

