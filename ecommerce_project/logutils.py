# logutils.py
import logging
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class BlueFormatter(logging.Formatter):
    def format(self, record):
        message = super().format(record)

        sql = record.sql.lower() if hasattr(record, "sql") else record.getMessage().lower()

        if sql.startswith('select'):
            color = Fore.BLUE
        elif sql.startswith('insert') or sql.startswith('update'):
            color = Fore.GREEN
        elif sql.startswith('delete'):
            color = Fore.RED
        else:
            color = Style.RESET_ALL

        return f"{color}{message}{Style.RESET_ALL}"
