import sys
from math import sqrt

d = {}
roz = []
indices = []
totalIndices = 0
c = 0
cc = 0
sooner = 0
later = 0
same = 0
total = 0

with open(sys.argv[1]) as data_file:    
	for line in data_file:
		word = line.rstrip()
		d[word] = c
		c += 1

with open(sys.argv[2]) as data_file:    
	for line in data_file:
		if line[:-1] in d:
			indices.append(cc)
			totalIndices += cc
			total += d[line[:-1]] - cc
			roz.append(d[line[:-1]] - cc)
			if d[line[:-1]] - cc > 0: 
				later += 1
			elif d[line[:-1]] - cc < 0:
				sooner += 1
			else:
				same += 1
			d.pop(line[:-1], None)
		#else:
		#	total += cc
		cc += 1

#for k in d.keys():
#	total -= d[k]

avg = total / cc
rozptyl = 0
for x in roz:
	rozptyl += (x - avg) ** 2

var = rozptyl / len(roz)
final = sqrt(var)

print('avg index: ' + str(totalIndices / len(indices)))
print('absolute: ' + str(total) + ' ' + str(sooner) + ' ' + str(later) + ' ' + str(same) + ' ' + str(len(roz)))
print('average: ' + str(avg) + ' ' + str(var))
print('deviation: ' + str(final))
