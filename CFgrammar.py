from itertools import *
from operator import itemgetter
from collections import deque

def prepareQueue(maxlength, maxsize):
	# priprav queue, vytvor vsetky slova pre zakladne neterminaly
	for i in range(1, maxsize+1):
		x = 'A'+str(i)
		queue.append((x, maxlength-i))
		if not x in rulez['Z']:
			rulez['Z'][x] = 1
		if not x in rulez:
			rulez[x] = {}
			for z in product(alpha, repeat=i):
				s = ''.join(z)
				rulez[x][s] = 1
		x = 'D'+str(i)
		queue.append((x, maxlength-i))
		if not x in rulez['Z']:
			rulez['Z'][x] = 1
		if not x in rulez:
			rulez[x] = {}
			for z in product(digit, repeat=i):
				s = ''.join(z)
				rulez[x][s] = 1
		x = 'S'+str(i)
		queue.append((x, maxlength-i))
		if not x in rulez['Z']:
			rulez['Z'][x] = 1
		if not x in rulez:
			rulez[x] = {}
			for z in product(special, repeat=i):
				s = ''.join(z)
				rulez[x][s] = 1

def createRules(maxsize):
	# dokym mas co, vytvaraj vsetky mozne zlozene neterminaly
	while queue:
		tmp = queue.popleft()
		for i in range(1,maxsize+1):
			if tmp[1]-i < 0:
				break
			else:
				if tmp[0][-2] == 'A':
					if tmp[0][-1] == str(maxsize):
						x = tmp[0]+'A'+str(i)
						queue.append((x, tmp[1]-i))
						rulez['Z'][x] = 1
				else:
					x = tmp[0]+'A'+str(i)
					queue.append((x, tmp[1]-i))
					rulez['Z'][x] = 1
				if tmp[0][-2] == 'D':
					if tmp[0][-1] == str(maxsize):
						x = tmp[0]+'D'+str(i)
						queue.append((x, tmp[1]-i))
						rulez['Z'][x] = 1
				else:
					x = tmp[0]+'D'+str(i)
					queue.append((x, tmp[1]-i))
					rulez['Z'][x] = 1
				if tmp[0][-2] == 'S':
					if tmp[0][-1] == str(maxsize):
						x = tmp[0]+'S'+str(i)
						queue.append((x, tmp[1]-i))
						rulez['Z'][x] = 1
				else:
					x = tmp[0]+'S'+str(i)
					queue.append((x, tmp[1]-i))
					rulez['Z'][x] = 1

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

maxlength = 8
maxsize = 4
koeficient = 1
alpha = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
digit = '0123456789'
special = "'~!@#$%^&*;,.-<>`_ "
queue = deque([])
rulez = {}
rulez['Z'] = {}
prepareQueue(maxlength,maxsize)
createRules(maxsize)
ruleCount={}
for rule in rulez:
	ruleCount[rule] = len(rulez[rule])
#print(ruleCount)
with open('john.txt') as f:
	for line in f:
		word = line.rstrip('\n')
		if len(word) > 0:
			updateMyrules(word)
with open('cain.txt') as f:
	for line in f:
		word = line.rstrip('\n')
		if len(word) > 0:
			updateMyrules(word)

#rc = sum(ruleCount.values())
for rule in rulez:
	for r in rulez[rule]:
		x = rulez[rule][r]
		rulez[rule][r] = float((x / ruleCount[rule]) * koeficient)

for x in rulez:
	rulez[x] = sorted(rulez[x].items(), key=itemgetter(1), reverse=True)

print(ruleCount)
for rule in rulez:
	print(rule + ":")
	for r in rulez[rule]:
		print("\t"+str(r[0])+"-"+"{0:.4f}".format(r[1]))
	print()
	print()

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
			notnull = False
			temp = self.chance
			for x in range(0, len(self.deti)):
				if (z[x] != 0):
					notnull = True
				if (self.deti[x]+z[x]) < 0 or (self.deti[x]+z[x]) >= len(rulez[str(self.net[2*x:2*(x+1)])]):
					break
				temp /= rulez[str(self.net[2*x:2*(x+1)])][self.deti[x]][1]
				temp *= rulez[str(self.net[2*x:2*(x+1)])][self.deti[x]+z[x]][1]
			else:
				#print(str(z) + " " + str(temp))
				if temp <= self.chance and temp > maximum and notnull:
					if temp == self.chance:
						if sum(z) >= 0:
							maximum = temp
							maxim = z
					else:
						maximum = temp
						maxim = z
		for i in range(0, len(self.deti)):
			#self.chance /= rulez[str(self.net[2*x:2*(x+1)])][self.deti[i]][1]
			self.deti[i] += maxim[i]
			#self.chance *= rulez[str(self.net[2*x:2*(x+1)])][self.deti[i]][1]
		self.chance = maximum
		return ret

nets=[]
for r in rulez['Z']:
	nets.append(Neterminal(r[0], [0] * (len(str(r[0]))//2)))

#print(nets[0].net)
#for i in range(0, 200):
#	print(nets[0].chance)
#	print(nets[0].next())
#	print()
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