from colorama import Fore
from api.utils.logger.error_levels.Level import Level


class WarningLevel(Level):
    def __init__(self):
        super().__init__()
        self.severity = "Warning"
        self.color = Fore.YELLOW
        self.severity_number = 2
