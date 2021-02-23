import os
import re
import sys

import pefile

argv = sys.argv
argc = len(argv)
stdout = sys.stdout

if(argc != 2):
    stdout.write('Usage: python TP2p2-1.py bin\n')
    stdout.write('or python TP2p2-1.py file.exe\n')
    exit(1)

inputPath = argv[1]


# ==============================================================================
# === FILE READING =============================================================

def openFile(filePath):
    try:
        return pefile.PE(filePath)
    except:
        stdout.write('Could not find file "{}"\n'.format(filePath))
        exit(1)

def getExeNameFromFilePath(filePath):
    appNameRegex = '\/?(\w*)\.exe$'
    return re.search(appNameRegex, filePath).group(1)

def isDirectory(path):
    return os.path.isdir(path)

def isExeFile(fileName):
    return fileName.endswith('.exe')

def getExeFilesPathsFromDirectory(directoryPath):
    filesNames = os.listdir(directoryPath)
    exeFilesNames = filter(isExeFile, filesNames)
    return [os.path.join(directoryPath, xmlFileName) for exeFileName in exeFilesNames]


# ==============================================================================
# === .EXE SECTION ANALYSIS ====================================================

def isExecutableSection(section):
    return getattr(section, 'IMAGE_SCN_MEM_EXECUTE')

def getExecutableSectionsFromFile(file):
    executableSections = []

    for section in file.sections:
        if isExecutableSection(section):
            executableSections.append(section.Name.decode("utf-8"))

    return executableSections


# ==============================================================================
# === PRINTING HELPERS =========================================================

def printHeader(title):
    stdout.write('===================\n\n')
    stdout.write('{}\n\n'.format(title))
    stdout.write('===================\n\n')

def printExecutableSections(exeName, executableSections):
    stdout.write('{}: {}\n\n'.format(exeName, executableSections))


# ==============================================================================
# === PROGRAM EXECUTION ========================================================

exeFiles = {}

def appendNewExeFile(filePath):
    exeName = getExeNameFromFilePath(filePath)
    exeFiles[exeName] = openFile(filePath)

if(isDirectory(inputPath)):
    for exeFilePath in getExeFilesPathsFromDirectory(inputPath):
        appendNewExeFile(exeFilePath)
else:
    appendNewExeFile(inputPath)


printHeader('Secoes Executaveis')
for exeName in sorted(exeFiles):
    file = exeFiles[exeName]

    executableSections = getExecutableSectionsFromFile(file)
    printExecutableSections(exeName, executableSections)
