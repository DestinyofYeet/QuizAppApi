from colorama import Fore
from api.utils.logger.error_levels.Level import Level


class ErrorLevel(Level):
    def __init__(self):
        super().__init__()
        self.severity = "ERROR"
        self.color = Fore.RED
        self.severity_number = 3
