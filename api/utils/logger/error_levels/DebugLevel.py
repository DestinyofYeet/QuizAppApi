from colorama import Fore
from api.utils.logger.error_levels.Level import Level


class DebugLevel(Level):
    def __init__(self):
        super().__init__()
        self.severity = "DEBUG"
        self.color = Fore.LIGHTWHITE_EX
        self.severity_number = 0
