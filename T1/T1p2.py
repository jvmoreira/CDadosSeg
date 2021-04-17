import sys

argv = sys.argv
argc = len(argv)
stdout = sys.stdout

PROTOCOLS_INDEXES = { 'ip': 0, 'tcp': 1, 'udp': 2, 'icmp': 3 }

if(argc != 3):
    stdout.write('Usage: python TP1p2.py community.rules sid-msg.map\n')


# ========================================================
# === SID MAP ============================================

sidMapFileName = argv[2]

sidMapFile = None

try:
    sidMapFile = open(sidMapFileName, 'r')
except:
    stdout.write('Could not find file "{}"\n'.format(sidMapFileName))
    exit(1)

sidMap = {}
for line in sidMapFile:
    sections = line.split('||')
    sid = sections[0].strip()
    message = sections[1].strip()

    sidMap[sid] = message

sidMapFile.close()

# ========================================================
# === RULES FILE READING =================================

rulesFileName = argv[1]

rulesFile = None
outputFile = open('T1p2.txt', 'w')

try:
    rulesFile = open(rulesFileName, 'r')
except:
    stdout.write('Could not find file "{}"\n'.format(rulesFileName))
    exit(1)

def isInvalidLine(line):
    return 'alert' not in line[0:7]

for line in rulesFile:
    if isInvalidLine(line):
        continue

    content = line.split('alert')[1:]
    # Junta o conteudo caso ele tenha sido dividido
    if len(content) > 1:
        content = 'alert'.join(content)
    else:
        content = content[0]
    content = content.strip()

    protocol = content.split(' ')[0]
    protocolIndex = PROTOCOLS_INDEXES.get(protocol)

    port = content.split('(')[0].strip().split(' ')[-1]

    sidNumber = content.split(' sid:')[1].split(';')[0]
    sidMessage = sidMap[sidNumber]

    outputFile.write('{},{},{}\n'.format(protocolIndex, port, sidMessage))

outputFile.close()
rulesFile.close()
