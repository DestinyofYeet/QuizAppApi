import os

from api.utils.logger.logger import Logger
from api.utils.meta.singleton import Singleton

logger = Logger()


class Config(metaclass=Singleton):  # just makes sure there only exists one copy of this class
    def __init__(self):
        """
        This is a class for all configuration this api_old may need
        """
        self.db_user: str = os.getenv("config_db_user")
        self.db_port: int = int(os.getenv("config_db_port"))
        self.db_server: str = os.getenv("config_db_server")
        self.db_password: str = os.getenv("config_db_password")
        self.db_table: str = os.getenv("config_db_table")

        self.api_port: int = int(os.getenv("config_api_port"))
        self.api_host: str = os.getenv("config_api_host")

        for var, value in vars(self).items():  # makes sure all variables were got from the environment table
            if value is None:
                logger.error(f"ERROR: Could not find 'config_{var}' in environment table")
                exit(1)
