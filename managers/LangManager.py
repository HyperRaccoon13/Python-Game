import json

from .ConfigManager import ConfigManager
from .Logger import Logger

class LangManager():
    def __init__(self, langFile, location):
        self.langFile = langFile
        self.location = location
        self.langData = self._LoadLang()
    

    def _LoadLang(self):
        try:
            with open(self.langFile, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            logger.error(f"The file {self.langFile} was not found.")
            return {}
        except json.JSONDecodeError:
            logger.error(f"JSON decoding failed. Please check the config file.")
            return {}
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return {}
        
    def GetLangkey(self, key, default=None):
        locatedData = self.langData.get(self.location, {})
        return locatedData.get(key, default)


configManager = ConfigManager("config.json")
logger = Logger("Lang Manager", logFile=configManager.GetConfigValues("logPath") + "/log.text", enabled=configManager.GetConfigValues("outputLog"))
logger.info("Logging Lang Manager")   

