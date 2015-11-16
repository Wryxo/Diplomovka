from itertools import *
from operator import itemgetter

def createRule(rule, count, last):
	maxi = maxsize
	if maxsize > count:
		maxi = count
	if count == 0:
		if not rule in rulez['Z']:
			rulez['Z'][rule] = 1
		return
	if last == 'A':
		for i in range(maxi, 0, -1):
			createRule(rule + 'D'+str(i), count-i, 'D')
			createRule(rule + 'S'+str(i), count-i, 'S')
	elif last == 'D':
		for i in range(maxi, 0, -1):
			createRule(rule + 'A'+str(i), count-i, 'A')
			createRule(rule + 'S'+str(i), count-i, 'S')
	elif last == 'S':
		for i in range(maxi, 0, -1):
			createRule(rule + 'A'+str(i), count-i, 'A')
			createRule(rule + 'D'+str(i), count-i, 'D')
	else:
		for i in range(maxi, 0, -1):
			createRule(rule + 'A'+str(i), count-i, 'A')
			x = 'A'+str(i)
			if not x in rulez:
				rulez[x] = {}
				for z in product(alpha, repeat=i):
					s = ''.join(z)
					rulez[x][s] = 1
			createRule(rule + 'D'+str(i), count-i, 'D')
			x = 'D'+str(i)
			if not x in rulez:
				rulez[x] = {}
				for z in product(digit, repeat=i):
					s = ''.join(z)
					rulez[x][s] = 1
			createRule(rule + 'S'+str(i), count-i, 'S')
			x = 'S'+str(i)
			if not x in rulez:
				rulez[x] = {}
				for z in product(special, repeat=i):
					s = ''.join(z)
					rulez[x][s] = 1

def updateMyrules(word):
	buf = 0
	current = 'A'
	rule = ''
	s=word[0]
	if word[0] in digit:
		current = 'D'
	if word[0] in special:
		current = 'S'
	for i in range(1, len(word)):
		if (word[i] in alpha) and (current != 'A'):
			rule += current + str(i-buf)
			rulez[current + str(i-buf)][str(s)] += 1
			ruleCount[current + str(i-buf)] += 1
			buf = i
			current = 'A'
			s=''
		elif (word[i] in digit) and (current != 'D'):
			rule += current + str(i-buf)
			rulez[current + str(i-buf)][str(s)] += 1
			ruleCount[current + str(i-buf)] += 1
			buf = i
			current = 'D'
			s=''
		elif (word[i] in special) and (current != 'S'):
			rule += current + str(i-buf)
			rulez[current + str(i-buf)][str(s)] += 1
			ruleCount[current + str(i-buf)] += 1
			buf = i
			current = 'S'
			s=''
		elif len(s) >= maxsize:
			rule += current + str(i-buf)
			rulez[current + str(i-buf)][str(s)] += 1
			ruleCount[current + str(i-buf)] += 1
			buf = i
			s=''
		s += word[i]
	rule += current + str(len(word)-buf)
	rulez[current + str(len(word)-buf)][str(s)] += 1
	ruleCount[current + str(len(word)-buf)] += 1
	if not rule in rulez['Z']:
		rulez['Z'][rule] = 0
	rulez['Z'][rule] += 1
	ruleCount['Z'] += 1

maxlength = 4
maxsize = 4
koeficient = 10000
alpha = 'abcdefghijklmnopqrstuvwxyz'
digit = '0123456789'
special = "'~!@#$%^&*;,.-<>`_ "
rulez = {}
rulez['Z'] = {}
for i in range(0,maxlength):
	createRule('', i+1, 'Z')
ruleCount={}
for rule in rulez:
	ruleCount[rule] = len(rulez[rule])
#print(ruleCount)
with open('johnLC.txt') as f:
	for line in f:
		word = line.rstrip('\n')
		if len(word) > 0:
			updateMyrules(word)

for rule in rulez:
	for r in rulez[rule]:
		x = rulez[rule][r]
		rulez[rule][r] = float((x / ruleCount[rule]) * koeficient)

for x in rulez:
	rulez[x] = sorted(rulez[x].items(), key=itemgetter(1), reverse=True)

#print(ruleCount)
#for rule in rulez:
	#print(rule + ":")
	#for r in rulez[rule]:
	#	print("\t"+str(r[0])+":"+"{0:.4f}".format(r[1]))
	#print()
	#print()

class Neterminal:
	deti=[]
	net=None
	chance=1

	def __init__(self, net, indexy):
		self.deti = indexy
		self.net = net
		for i in range(0, len(indexy)):
			self.chance *= rulez[str(net[2*i:2*(i+1)])][indexy[i]][1]

	def next(self):
		ret=''
		for i in range(0, len(self.deti)):
			ret += str(rulez[str(self.net[2*i:2*(i+1)])][self.deti[i]][0])

		maximum = -1
		maxim = []
		for z in product([-1, 0, 1], repeat=len(self.deti)):
			temp = 1
			for x in range(0, len(self.deti)):
				if (self.deti[x]+z[x]) < 0:
					break
				temp *= rulez[str(self.net[2*x:2*(x+1)])][self.deti[x]+z[x]][1]
			else:
				if temp < self.chance and temp > maximum:
					maximum = temp
					maxim = z
		for i in range(0, len(self.deti)):
			self.chance /= rulez[str(self.net[2*x:2*(x+1)])][self.deti[i]][1]
			self.deti[i] += maxim[i]
			self.chance *= rulez[str(self.net[2*x:2*(x+1)])][self.deti[i]][1]
		return ret

nets=[]
for r in rulez['Z']:
	nets.append(Neterminal(r[0], [0] * (len(str(r[0]))//2)))

print(rulez['A4'])
print(rulez['A2'])
print(nets[0].net)
for i in range(0, 20):
	print(nets[0].next())
	print(nets[0].chance)
#curr = 0
#for i in range(0,10):
#	cc = nets[curr].chance * rulez['Z'][curr][1]
#	pc = -1
#	nc = -1
#	ncurr = 0
#	print(nets[curr].next())
#	if curr < len(nets)-1:
#		n = nets[curr+1]
#		nc = n.chance * rulez['Z'][curr+1][1]
#		if (nc > cc):
#			ncurr = 1
#	if curr > 0:
#		p = nets[curr-1]
#		pc = p.chance * rulez['Z'][curr-1][1]
#		if (pc > cc):
#			ncurr = -1
#	print(pc)
#	print(cc)
#	print(nc)
#	curr += ncurr