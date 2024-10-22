import json
import customtkinter as ctk
import os

class ConfigManager:
    def __init__(self, configFile):
        self.configFile = configFile
        self.configData = self._LoadConfig()

    def _LoadConfig(self):
        try:
            with open(self.configFile, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: The file {self.configFile} was not found.")
            return {}
        except json.JSONDecodeError:
            print("Error: JSON decoding failed. Please check the config file.")
            return {}
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return {}
        
    def GetConfigValues(self, key, default=None):
        return self.configData.get(key, default)
    
    def GetWindowSize(self, windowType, split=False):
        sizeString = self.configData.get("windowSize", {}).get(windowType, "800x600")
        try:
            xString, yString = sizeString.split("x")
            x = int(xString)
            y = int(yString)
        except (ValueError, TypeError):
            x, y = 800, 600

        if split:
            return x, y
        else: return f"{x}x{y}"