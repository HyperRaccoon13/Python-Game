import datetime
import os

class Logger():
    LEVELS = {
        "DEBUG": 0, 
        "INFO": 1,
        "WARN": 2,
        "ERROR": 3,
        "FATAL": 4
    }
    
    COLORS = {
        "RESET": "\033[0m",
        "DEBUG": "\033[94m", #Green
        "INFO":  "\033[92m", #Blue
        "WARN":  "\033[93m", #Yello
        "ERROR": "\033[91m", #Red
        "FATAL": "\033[41m"  #Red Background
    }

    def __init__(self, name, level="INFO", logFile=None, enabled=False):
        self.name = name
        self.level = self.LEVELS.get(level.upper(), 1)
        self.logFile = logFile
        self.enabled = enabled

        if logFile:
            os.makedirs(os.path.dirname(logFile), exist_ok=True)


    def log(self, message, level="INFO"):
        if not self.enabled:
            return

        level = level.upper()
        if self.LEVELS.get(level, 1) >= self.level:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            color = self.COLORS.get(level, self.COLORS["RESET"])
            logMessage = f"{color}[{timestamp}] [{self.name}] [{level}] {message}{self.COLORS['RESET']}"
            print(logMessage)

            outputLogMessage = f"[{timestamp}] [{self.name}] [{level}] {message}"
            if self.logFile:
                with open(self.logFile, "a") as file:
                    file.write(outputLogMessage + "\n")

    def debug(self, message):
        self.log(message, level="DEBUG")

    def info(self, message):
        self.log(message, level="INFO")

    def warn(self, message):
        self.log(message, level="WARN")

    def error(self, message):
        self.log(message, level="ERROR")

    def fatal(self, message):
        self.log(message, level="FATAL")