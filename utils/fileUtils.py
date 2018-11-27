import os, json

ICONPATH = os.path.dirname(__file__).replace("utils", "icons") + "/"
configPath = os.path.dirname(__file__) + "\\config.json"

def getIcon(iconName):
    fileList = os.listdir(ICONPATH)

    if iconName in fileList:
        return ICONPATH + iconName

    return False

def getMovieFiles(folderPath):
    files = [folderPath + "/" + i for i in os.listdir(unicode(folderPath)) if i.lower().endswith(".mkv")]
    return files

def saveConfig(dict):
    with open(configPath, "w") as configFile:
        json.dump(dict, configFile)

def loadConfig():
    if os.path.exists(configPath):
        with open(configPath) as configFile:
            return json.load(configFile)
    else:
        return {}