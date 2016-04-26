import sys
from infinario import Infinario

# inputDictionary outputWordlist
lines = 0
vyskyty = 0
inputDict = {}

with open(sys.argv[1]) as f:
	for line in f:
		line = line.split(' ', 1)
		if not line[1] in inputDict:
			inputDict[line[1]] = (lines, int(line[0]))
		lines += 1
		vyskyty += int(line[0])

found = 0
count = 0
res = 0
uzBoli = {}

i = 1
with open(sys.argv[2]) as f:
	for line in f:
		if line in inputDict:
			if not line in uzBoli:
				uzBoli[line] = 1
				found += 1
				res += (inputDict[line][1] / vyskyty) * (count - inputDict[line][0])
		count += 1
			
print(res / found)