import json

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
            print(f"Error: The file {self.langFile} was not found.")
            return {}
        except json.JSONDecodeError:
            print("Error: JSON decoding failed. Please check the config file.")
            return {}
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return {}
        
    def GetLangkey(self, key, default=None):
        locatedData = self.langData.get(self.location, {})
        return locatedData.get(key, default)
        

