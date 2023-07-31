import gkeepapi
import os

keep = gkeepapi.Keep()
keep.login('email@gmail.com', 'password')

def getFiles(dirPath):
    files = {}

    for filePath in os.listdir(dirPath):
        fullPath = os.path.join(dirPath, filePath)
        if os.path.isfile(fullPath):
            fileContent = open(fullPath, encoding = 'utf-8', mode = 'r')
            files[filePath.split('.')[0]] = fileContent.read()

    return files

def createKeeps(files):
    labelName = os.getenv('LABEL')

    if not files:
        return False
    else:
        label = keep.findLabel(labelName)
        if not label: 
            label = keep.createLabel(labelName)
        for noteName in files:
            if not keep.find(query = noteName):
                note = keep.createNote(noteName, files[noteName])
                note.labels.add(label)

def main(): 
    dirPath = os.getenv('PATH')

    files = getFiles(dirPath)

    createKeeps(files)

    keep.sync()

if __name__ == '__main__':
    main()