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
    
    def __init__(self, name, level="INFO", logFile=None):
        self.name = name
        self.level = self.LEVELS.get(level.upper(), 1)
        self.logFile = logFile

        if logFile:
            os.makedirs(os.path.dirname(logFile), exist_ok=True)


    def log(self, message, level="INFO"):
        level = level.upper()
        if self.LEVELS.get(level, 1) >= self.level:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logMessage = f"[{timestamp}] [{self.name}] [{level}] {message}"

            print(logMessage)

            if self.logFile:
                with open(self.logFile, "a") as file:
                    file.write(logMessage + "\n")

    def debug(self, message):
        self.log(message, level="DEBUG")

    def info(self, message):
        self.log(message, level="INFO")

    def warning(self, message):
        self.log(message, level="WARNING")

    def error(self, message):
        self.log(message, level="ERROR")

    def critical(self, message):
        self.log(message, level="CRITICAL")