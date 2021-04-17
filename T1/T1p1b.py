import sys

argv = sys.argv
argc = len(argv)
stdout = sys.stdout

if(argc != 2):
    stdout.write('Usage: python TP1p1b.py file.txt\n')

inputFileName = argv[1]

inputFile = None

try:
    inputFile = open(inputFileName, 'r')
except:
    stdout.write('Could not find file "{}"\n'.format(inputFileName))
    exit(1)

outputFile = open('T1p1b.txt', 'w')

for line in inputFile:
    splitByDot = line.split('.')

    field1 = splitByDot[1]
    field2 = splitByDot[2]
    field3_4 = splitByDot[3].split('-')

    field3 = field3_4[0]
    field4 = field3_4[1].split(':')[0]

    outputFile.write('{},{},{},{}\n'.format(field1, field2, field3, field4))

outputFile.close()
inputFile.close()
