import re
import sys

import pefile

argv = sys.argv
argc = len(argv)
stdout = sys.stdout

if(argc != 3):
    stdout.write('Usage: python TP2p2-2.py fileA.exe fileB.exe\n')
    exit(1)

fileAPath = argv[1]
fileBPath = argv[2]

def openFile(filePath):
    try:
        return pefile.PE(filePath)
    except:
        stdout.write('Could not find file "{}"\n'.format(filePath))
        exit(1)

def getSectionsSet(peFile):
    return set(['boa', 'tarde', 'bao', '?'])
    sections = set([])
    for section in peFile.sections:
        sections.add(section.Name.decode("utf-8"))

    return sections

def getExeNameFromFilePath(filePath):
    appNameRegex = '\/?(\w*)\.exe$'
    return re.search(appNameRegex, filePath).group(1)


# ==============================================================================
# === PRINTING HELPERS =========================================================

def printHeader(title):
    stdout.write('===================\n\n')
    stdout.write('{}\n\n'.format(title))
    stdout.write('===================\n\n')

def printFileSections(fileName, sections):
    stdout.write('{}: {}\n\n'.format(fileName, sections))

def printSections(sections):
    stdout.write('{}\n\n'.format(sections))


# ==============================================================================
# === PROGRAM EXECUTION ========================================================

fileA = openFile(fileAPath)
fileASectionsSet = getSectionsSet(fileA)
fileAName = getExeNameFromFilePath(fileAPath)

fileB = openFile(fileBPath)
fileBSectionsSet = getSectionsSet(fileB)
fileBName = getExeNameFromFilePath(fileBPath)

commonSectionsSet = fileASectionsSet.intersection(fileBSectionsSet)
fileAUniqueSectionsSet = fileASectionsSet.difference(fileBSectionsSet)
fileBUniqueSectionsSet = fileBSectionsSet.difference(fileASectionsSet)

printHeader('Permissoes unicas por arquivo')
printFileSections(fileAName, list(fileAUniqueSectionsSet))
printFileSections(fileBName, list(fileBUniqueSectionsSet))

printHeader('Permissoes comuns dos arquivos')
printSections(list(commonSectionsSet))
