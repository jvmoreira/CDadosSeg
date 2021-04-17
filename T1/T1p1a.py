import sys

argv = sys.argv
argc = len(argv)
stdout = sys.stdout

if(argc != 2):
    stdout.write('Usage: python TP1p1a.py file.txt\n')

inputFileName = argv[1]

inputFile = None

try:
    inputFile = open(inputFileName, 'r')
except:
    stdout.write('Could not find file "{}"\n'.format(inputFileName))
    exit(1)

variantsByKindAndFamily = {}

def addVariant(kind, family, variant):
    if not variantsByKindAndFamily.has_key(kind):
        variantsByKindAndFamily[kind] = {}

    if not variantsByKindAndFamily[kind].has_key(family):
        variantsByKindAndFamily[kind][family] = []

    if not variant in variantsByKindAndFamily[kind][family]:
        variantsByKindAndFamily[kind][family].append(variant)

def getLabel(line):
    sections = line.split(':')
    label = sections[2]
    return label

def isInvalidLabel(label):
    return (label.count('.') != 2) or ('-' not in label)

def getLabelAttributes(label):
    _, kind, code = label.split('.')
    sections = code.split('-')
    family = sections[0]
    variant = sections[1]
    return [kind, family, variant.strip()]

for line in inputFile:
    label = getLabel(line)

    if isInvalidLabel(label):
        continue

    [kind, family, variant] = getLabelAttributes(label)

    addVariant(kind, family, variant)

outputFile = open('T1p1a.txt', 'w')

for kind in sorted(variantsByKindAndFamily):
    familyDict = variantsByKindAndFamily[kind]
    for family in sorted(familyDict):
        variants = familyDict[family]
        outputFile.write('{}.{},{}\n'.format(kind, family, len(variants)))

outputFile.close()
inputFile.close()
