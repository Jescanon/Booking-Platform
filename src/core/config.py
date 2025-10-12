import os
from dotenv import load_dotenv
from alembic import context

config = context.config

load_dotenv()
infos = dict(os.environ)

class Config:
    def __init__(self, **args):
        self.info = dict()

        inf = ["ENGINE",
               "USER",
               "PASSWORD",
               "BASE_NAME",
               "DOMAIN",
               ]

        for key in args:
            if key in inf:
                self.info.update({key: args[key]})

    def get_engine_db(self):
        return f"{self.info['ENGINE']}://{self.info['USER']}:{self.info['PASSWORD']}@{self.info['DOMAIN']}/{self.info['BASE_NAME']}"

configs = Config(**infos)

config.set_main_option("sqlalchemy.url", configs.get_engine_db())

