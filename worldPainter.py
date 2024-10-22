import pygame
import customtkinter
import os
import re
from managers import ConfigManager, AssetManager, LangManager, Logger

screenX = 1920
screenY = 1080


def GetWorlds():
    return [file for file in os.listdir(configManager.GetConfigValues("worldPath")) if file.endswith(".txt")]

def CheckVaildPath(filename):
    invalidCharPattern = r'[<>:"/\\|?*]'
    invalidNamePattern = r'^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])$'

    if re.search(invalidCharPattern, filename):
        return False
    
    if re.search(invalidNamePattern, filename, re.IGNORECASE):
        return False
    
    return True

def GetSettingsFromWorld(world):
    settingPattern = r'Settings:\(([^)]+)\)'

    settingMatch = re.search(settingPattern, world)

    if not settingMatch:
        return None
    
    settingContent = settingMatch.group(1)

    keyPairs = settingContent.split(",")

    settingsDict = {}

    for pair in keyPairs:
        key, value = pair.split(":")
        settingsDict[key.strip()] = value.strip()

    return settingsDict


class NewWorldPannel(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
    
        self.fileNameLabel = customtkinter.CTkLabel(self, text=langManager.GetLangkey("text.fileNameLabel"))
        self.fileNameLabel.grid(row=0, column=0, padx=5, pady=5)

        self.fileNameTextbox = customtkinter.CTkTextbox(self, width=200, height=50)
        self.fileNameTextbox.grid(row=0, column=1, padx=5, pady=5)

        self.tileSheetPathLabel = customtkinter.CTkLabel(self, text=langManager.GetLangkey("text.tileSheetPathLabel"))
        self.tileSheetPathLabel.grid(row=1, column=0, padx=5, pady=5)

        self.tileSheetPathTextBox = customtkinter.CTkTextbox(self, width=200, height=50)
        self.tileSheetPathTextBox.grid(row=1, column=1, padx=5, pady=5)

        self.advancedSettingDefaultValue = customtkinter.StringVar(value=False)
        self.advancedSettingCheckBox = customtkinter.CTkCheckBox(self, text=langManager.GetLangkey("text.advancedSettingCheckBox"), variable=self.advancedSettingDefaultValue,
                                                                onvalue=True, offvalue=False, command=self.AdvancedSettingToggle)
        
        self.advancedSettingCheckBox.grid(row=2, column=0, padx=5, pady=5)

        self.advancedSettingTextBox = customtkinter.CTkTextbox(self, width=200, height=50)

        self.createWorldButton = customtkinter.CTkButton(self, text=langManager.GetLangkey("text.createWorldButton"), command=self.CreateWorldButtonCallBack)
        self.createWorldButton.grid(row=3, column=0, padx=5, pady=5)

        self.errorMessageLabel = customtkinter.CTkLabel(self, text="", text_color="red")
        self.errorMessageLabel.grid(row=3, column=1, padx=5, pady=5)

    def AdvancedSettingToggle(self):
        if self.advancedSettingDefaultValue.get() == "1":
            self.advancedSettingTextBox.grid(row=2, column=1, padx=5, pady=5)
        else:
            self.advancedSettingTextBox.grid_forget()

    def CreateWorldButtonCallBack(self):
        fileNameInput = self.fileNameTextbox.get("0.0", "end").strip()
        tileSheetInput = self.tileSheetPathTextBox.get("0.0", "end").strip()
        worldFilePath = f"{configManager.GetConfigValues('worldPath')}/{fileNameInput}"


        if CheckVaildPath(fileNameInput) and CheckVaildPath(tileSheetInput) and not os.path.exists(worldFilePath):
            self.errorMessageLabel.configure(text=langManager.GetLangkey("text.errorMessageLabel"), text_color="white")
            with open(worldFilePath+".txt", "w") as file:

                if self.advancedSettingDefaultValue.get() == "1":
                    advancedSettingsInput = self.advancedSettingTextBox.get("0.0", "end").strip()
                    file.write(advancedSettingsInput)

                elif tileSheetInput == "" or None:
                    file.write("(Settings:(tileSet:assets/world/tileSet.png, sizeX:100, sizeY:100, cellSize:16))")
                else:
                    file.write(f"(Settings:(tileSet:{tileSheetInput}, sizeX:100, sizeY:100, cellSize:16))")

        elif fileNameInput == "" or None:
            self.errorMessageLabel.configure(text=langManager.GetLangkey("warn.errorMessageLabel.0"))

        elif os.path.exists(worldFilePath):
            self.errorMessageLabel.configure(text=langManager.GetLangkey("warn.errorMessageLabel.2"))
        else: 
            self.errorMessageLabel.configure(text=langManager.GetLangkey("warn.errorMessageLabel.3"))

class EditWorldPannel(customtkinter.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)


        self.worldSelectionDefaultText = customtkinter.StringVar(value="Select a World")
        self.worldSelectionOptionMenu = customtkinter.CTkOptionMenu(self, variable=self.worldSelectionDefaultText, values=GetWorlds(), command=self.UpdateButton)
        self.worldSelectionOptionMenu.grid(row=0, column=0,  padx=5, pady=5)

        self.worldSelectionButton = customtkinter.CTkButton(self, text="Load World", state="disabled")
        self.worldSelectionButton.grid(row=0, column=1,  padx=5, pady=5)

    def UpdateButton(self, selectedWorld):
        if selectedWorld and selectedWorld != "Select a World":
            self.worldSelectionButton.configure(state="normal")

class ToolBarFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.newWorldButton = customtkinter.CTkButton(self, text=langManager.GetLangkey("text.newWorldButton"), command=self.OpenNewWorldPannel)
        self.newWorldButton.pack(side="left", padx=5)

        self.editWorldButton = customtkinter.CTkButton(self, text=langManager.GetLangkey("text.editWorldButton"), command=self.OpenEditWorldPannel)
        self.editWorldButton.pack(side="left", padx=5)

    def OpenNewWorldPannel(self):
        newWorldPannel = NewWorldPannel(self)
        newWorldPannel.grab_set()

    def OpenEditWorldPannel(self):
        openEditWorldPannel = EditWorldPannel(self)
        openEditWorldPannel.grab_set()

class DrawingFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

class PropertiesFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


class WorldPainter(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry(f"{screenX}x{screenY}")


        self.toolBarFrame = ToolBarFrame(master=self, height=50)
        self.toolBarFrame.pack(padx=5, side="top", fill="x")
        self.toolBarFrame.pack_propagate(False)
        
        self.drawFrame = DrawingFrame(master=self, width=screenX-200)
        self.drawFrame.pack(padx=5, pady=10, side="left", fill="both")

        self.propertiesFrame = PropertiesFrame(master=self, width=200)
        self.propertiesFrame.pack(padx=5, pady=10, side="right", fill="y")



configManager = ConfigManager("config.json")
assetManager = AssetManager(configManager.GetConfigValues("assetsPath"))
langManager = LangManager(configManager.GetConfigValues("langPath"), "worldPainter")
logger = Logger("WorldPainter", logFile=configManager.GetConfigValues("logPath") + "/log.text")


WorldPainter = WorldPainter()
WorldPainter.mainloop()



