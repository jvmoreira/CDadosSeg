import os
import re
import sys

argv = sys.argv
argc = len(argv)
stdout = sys.stdout

if(argc != 2):
    stdout.write('Usage: python TP2p1.py manifests\n')
    exit(1)

manifestsDirectory = argv[1]


# ==============================================================================
# === FILE READING =============================================================

def isXmlFile(fileName):
    return fileName.endswith('.xml')

def getXmlFilesPathsFromDirectory(directoryPath):
    try:
        filesNames = os.listdir(directoryPath)
        xmlFilesNames = filter(isXmlFile, filesNames)
        return [os.path.join(directoryPath, xmlFileName) for xmlFileName in xmlFilesNames]
    except:
        stdout.write('Could not find directory "{}"\n'.format(directoryPath))
        exit(1)

def getAppNameFromFilePath(filePath):
    appNameRegex = 'AndroidManifest_(.*)\.xml$'
    return re.search(appNameRegex, filePath).group(1)

def isPermissionTag(string):
    usesPermissionTagRegex = '^<uses-permission .*/>$'
    return re.search(usesPermissionTagRegex, string.strip()) is not None

def getPermissionsFromManifestFile(manifestFile):
    permissions = []
    permissionRegex = 'android.permission\.(\w*)"'
    for line in manifestFile:
        if not isPermissionTag(line):
            continue

        permissionSearch = re.search(permissionRegex, line)
        if permissionSearch is not None:
            permissions.append(permissionSearch.group(1))

    return permissions


# ==============================================================================
# === PRINTING HELPERS =========================================================

def printHeader(title):
    stdout.write('===================\n\n')
    stdout.write('{}\n\n'.format(title))
    stdout.write('===================\n\n')

def printPermissions(permissions):
    stdout.write('{}\n\n'.format(permissions))

def printAppPermissions(appName, permissions):
    stdout.write('{}: {}\n\n'.format(appName, permissions))


# ==============================================================================
# === PROGRAM EXECUTION ========================================================

appsPermissions = {}

# Reads every manifest file
for manifestFilePath in getXmlFilesPathsFromDirectory(manifestsDirectory):
    appName = getAppNameFromFilePath(manifestFilePath)
    manifestFile = open(manifestFilePath, 'r')

    appPermissions = getPermissionsFromManifestFile(manifestFile)
    appsPermissions[appName] = appPermissions

    manifestFile.close()


# Printing permissions

printHeader('Permissoes por APK')
for appName in sorted(appsPermissions):
    appPermissions = appsPermissions[appName]
    printAppPermissions(appName, appPermissions)

printHeader('Permissoes unicas por APK')
for appName in sorted(appsPermissions):
    appPermissions = appsPermissions[appName]

    allOtherPermissions = []
    for [appToCheckName, permissionsToCheck] in appsPermissions.items():
        if appToCheckName == appName:
            continue

        allOtherPermissions += permissionsToCheck

    uniquePermissions = [permission for permission in appPermissions if permission not in allOtherPermissions]
    printAppPermissions(appName, uniquePermissions)


printHeader('Permissoes comuns das APKs')
allPermissionsLists = [set(permissionsList) for permissionsList in appsPermissions.values()]
commonPermissions = set.intersection(*allPermissionsLists)
printPermissions(list(commonPermissions))
