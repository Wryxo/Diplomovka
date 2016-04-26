import sys
import random
import itertools
import bisect
import os.path
import json
import ast

tt = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+=?'~!@#$%^&*:;,.-<>`_ "
abc = 'abcdefghijklmnopqrstuvwxyz\n "'+tt
chance = {}
prefix = ''
order = 4

if len(sys.argv) < 3:
	print("inputfile wordCount [order]")
	sys.exit()
cont = 'x'
if (os.path.isfile(sys.argv[1]+'.ls')):
	print("Session for this grammar found, continue ? y/n", file=sys.stderr)
	while cont != 'n' and cont != 'y': 
		cont = sys.stdin.read(1)
# UCENIE
c = 0
if (len(sys.argv) > 3):
	order = int(sys.argv[3])
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
					chance[prefix] = [0] * len(abc)
				chance[prefix][abc.index(x)] += int(parts[0])
				prefix = prefix[1:] + x

# GENEROVANIE

# najdi prvy prefix (ten s najvyssim poctom vyskytov ?)
word = ''
prefix = ''
biggest = -1
count = int(sys.argv[2])

for k,v in chance.items():
	s = sum(v) 
	if s > biggest:
		biggest = s
		word = k
		prefix = k
	for i in range(len(v)):
		chance[k][i] = chance[k][i] / s

if (cont == 'y'):
	with open(sys.argv[1]+'.ls') as data_file:    
		pq = ast.literal_eval(data_file.readline())
		random.setstate(pq)
# zacni generovat
c = 0
try:
	while True:
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
		if prefix in chance:
			cumdist = list(itertools.accumulate(chance[prefix]))
		else:
			cumdist = range(len(abc))
		x = random.random() * cumdist[-1]
		i = bisect.bisect(cumdist, x)
		word += abc[i]
		prefix = prefix[1:] + abc[i]

	with open(sys.argv[1]+'.ls', 'w') as outfile:
		outfile.write(str(random.getstate()))
	print('Session saved', file=sys.stderr)
	sys.exit(0)
except KeyboardInterrupt:
	with open(sys.argv[1]+'.ls', 'w') as outfile:
		outfile.write(str(random.getstate()))
	print('Session saved', file=sys.stderr)
	sys.exit(0)
