import sys
import random
import itertools
import bisect
import os.path
import json
import ast
from memory_profiler import profile

@profile
def getOccurences():
	c = 0
	prefix = ''
	with open(sys.argv[1]) as f:
		for line in f:
			c += 1
			parts = line.split(' ', 1)
			for x in parts[1]:
				if not x in abc:
					continue
				if len(prefix) < order:
					prefix += x
					continue
				else:
					if not prefix in chance:
						chance[prefix] = {}
					if not x in chance[prefix]:
						chance[prefix][x] = 0
					chance[prefix][x] += int(parts[0])
					prefix = prefix[1:] + x

@profile
def generateWords(prefix, word, delta, epsilon, maximum):
	c = 0
	while True:
		if len(word) >= maximum:
			word += '\n'
		if '\n' in word:
			print(word, end="")
			c += 1
			word = ''
		elif ' ' in word:
			print(word)
			c += 1
			word = ''
		if c > count:
			break
		chances = []
		if prefix in chance:
			for s in abc:
				tmp = prefix[1:] + s
				if s in chance[prefix]:
					chances.append(chance[prefix][s])
				elif tmp in chance:
					chances.append(delta)
				elif s in ' \n':
					chances.append(delta)
				else:
					chances.append(epsilon)
		else:
			for s in abc:
				tmp = prefix[1:] + s
				if tmp in chance:
					chances.append(delta)
				elif s in ' \n':
					chances.append(delta)
				else:
					chances.append(epsilon)
		cumdist = list(itertools.accumulate(chances))
		x = random.random() * cumdist[-1]
		i = bisect.bisect(cumdist, x)
		word += abc[i]
		prefix = prefix[1:] + abc[i]

if len(sys.argv) < 4:
	print("inputfile wordCount maxLength [order]")
	sys.exit()

abc = 'abcdefghijklmnopqrstuvwxyz\n ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+=?\'~!@#$%^&*:;,.-<>"`_'
chance = {}
order = 4

cont = 'x'
if (os.path.isfile(sys.argv[1]+'.ls')):
	print("Session for this grammar found, continue ? y/n", file=sys.stderr)
	while cont != 'n' and cont != 'y': 
		cont = sys.stdin.read(1)
# UCENIE
if (len(sys.argv) > 4):
	order = int(sys.argv[4])
getOccurences()

# GENEROVANIE

# najdi prvy prefix (ten s najvyssim poctom vyskytov ?)
word = ''
prefix = ''
biggest = -1
count = int(sys.argv[2])
epsilon = 1000 # Pravdepodobnost pre prechod zo znameho do neznameho stavu

for k,v in chance.items():
	s = sum(v.values()) 
	if s > biggest:
		biggest = s
		word = k
		prefix = k
	for i in v.keys():
		chance[k][i] = chance[k][i] / s
		if chance[k][i] < epsilon:
			epsilon = chance[k][i]

if (cont == 'y'):
	with open(sys.argv[1]+'.ls') as data_file:    
		pq = ast.literal_eval(data_file.readline())
		random.setstate(pq)
# zacni generovat
delta = epsilon * 10 # Pravdepodobnost pre prechod z neznameho do znameho stavu
try:
	generateWords(prefix, word, delta, epsilon, sys.argv[3])

	with open(sys.argv[1]+'.ls', 'w') as outfile:
		outfile.write(str(random.getstate()))
	print('Session saved', file=sys.stderr)
	sys.exit(0)
except KeyboardInterrupt:
	with open(sys.argv[1]+'.ls', 'w') as outfile:
		outfile.write(str(random.getstate()))
	print('Session saved', file=sys.stderr)
	sys.exit(0)
