import os
import pathlib

def createDir(path):
    try: 
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

def dirExists(directory):
    if(os.path.exists(directory)):
        print(f"\"{directory}\" already exists.")
        return True
    else:
        createDir(directory)

def writeToFile(content, fileName, modes = 'w'):
    with open(fileName, modes) as f:
        f.write(content)

