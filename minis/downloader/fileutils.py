import os

def createDir(path):
    try:
        os.mkdir(path)
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

