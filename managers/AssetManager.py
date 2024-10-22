from PIL import Image
import os

from .ConfigManager import ConfigManager
from .Logger import Logger

class AssetManager():
    def __init__(self, assetDirectory):
        self.assetDirectory = assetDirectory
        self.assetDictionary = self._createAssetDict()
        self.loadedAssets = {}
        self.LoadAssets()

    def _createAssetDict(self):
        assetDictionary = {}

        for root, dirs, files in os.walk(self.assetDirectory):
            for file in files:
                filePath = os.path.join(root, file)
                assetName, _ = os.path.splitext(file)
                assetDictionary[assetName] = filePath
        return assetDictionary
    
    def LoadAssets(self):
        for name, path in self.assetDictionary.items():
            try:
                if not os.path.exists(path):
                    logger.warn(f"File not found at {path}")
                    continue
                image = Image.open(path)
                self.loadedAssets[name] = image
            except Exception as e:
                logger.error(f"Failed to load image at {path}. Error: {e}")


    def GetAsset(self, name):
        return self.loadedAssets.get(name)
    
configManager = ConfigManager("config.json")
logger = Logger("Asset Manager", logFile=configManager.GetConfigValues("logPath") + "/log.text", enabled=configManager.GetConfigValues("outputLog"))
logger.info("Logging Asset Manager") 