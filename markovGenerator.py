import sys
import random
import itertools
import bisect
#+=?~!@#$%^&*
tt = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,'*!;)(#+=~@#$%^&"
abc = 'abcdefghijklmnopqrstuvwxyz\n "'+tt
chance = {}
prefix = ''
order = 5

# UCENIE
with open(sys.argv[1]) as f:
	for line in f:
		parts = line.split(' ', 1)
		for x in parts[1]:
		#for x in line:
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
count = 100000

for k,v in chance.items():
	s = sum(v) 
	if s > biggest:
		biggest = s
		word = k
		prefix = k
	for i in range(len(v)):
		chance[k][i] = chance[k][i] / s

# zacni generovat
c = 0
while True:
	if '\n' in word or ' ' in word:
		print(word, end="")
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
