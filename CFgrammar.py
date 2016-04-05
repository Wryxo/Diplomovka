from itertools import *
from operator import itemgetter
from collections import deque
import heapq
import copy
import json
import sys

def prepareQueue(maxpasslength, maxnetsize):
	# priprav queue, vytvor vsetky slova pre zakladne neterminaly
	for i in range(1, maxnetsize+1):
		x = 'A'+str(i)
		queue.append((x, maxpasslength-i))
		if not x in rulez['Z']:
			rulez['Z'][x] = 1
		if not x in rulez:
			rulez[x] = {}
			for z in product(lower, repeat=i):
				s = ''.join(z)
				rulez[x][s] = 1
		x = 'U'+str(i)
		queue.append((x, maxpasslength-i))
		if not x in rulez['Z']:
			rulez['Z'][x] = 1
		if not x in rulez:
			rulez[x] = {}
			for z in product(upper, repeat=i):
				s = ''.join(z)
				rulez[x][s] = 1
		x = 'D'+str(i)
		queue.append((x, maxpasslength-i))
		if not x in rulez['Z']:
			rulez['Z'][x] = 1
		if not x in rulez:
			rulez[x] = {}
			for z in product(digit, repeat=i):
				s = ''.join(z)
				rulez[x][s] = 1
		x = 'S'+str(i)
		queue.append((x, maxpasslength-i))
		if not x in rulez['Z']:
			rulez['Z'][x] = 1
		if not x in rulez:
			rulez[x] = {}
			for z in product(special, repeat=i):
				s = ''.join(z)
				rulez[x][s] = 1

def createRules(maxnetsize):
	# dokym mas co, vytvaraj vsetky mozne zlozene neterminaly
	while queue:
		tmp = queue.popleft()
		for i in range(1,maxnetsize+1):
			if tmp[1]-i < 0:
				break
			else:
				if tmp[0][-2] == 'A':
					if tmp[0][-1] == str(maxnetsize):
						x = tmp[0]+'A'+str(i)
						queue.append((x, tmp[1]-i))
						rulez['Z'][x] = 1
				else:
					x = tmp[0]+'A'+str(i)
					queue.append((x, tmp[1]-i))
					rulez['Z'][x] = 1
				if tmp[0][-2] == 'U':
					if tmp[0][-1] == str(maxnetsize):
						x = tmp[0]+'U'+str(i)
						queue.append((x, tmp[1]-i))
						rulez['Z'][x] = 1
				else:
					x = tmp[0]+'U'+str(i)
					queue.append((x, tmp[1]-i))
					rulez['Z'][x] = 1
				if tmp[0][-2] == 'D':
					if tmp[0][-1] == str(maxnetsize):
						x = tmp[0]+'D'+str(i)
						queue.append((x, tmp[1]-i))
						rulez['Z'][x] = 1
				else:
					x = tmp[0]+'D'+str(i)
					queue.append((x, tmp[1]-i))
					rulez['Z'][x] = 1
				if tmp[0][-2] == 'S':
					if tmp[0][-1] == str(maxnetsize):
						x = tmp[0]+'S'+str(i)
						queue.append((x, tmp[1]-i))
						rulez['Z'][x] = 1
				else:
					x = tmp[0]+'S'+str(i)
					queue.append((x, tmp[1]-i))
					rulez['Z'][x] = 1

def updateMyrules(word, occ=1):
	buf = 0
	current = 'A'
	rule = ''
	s=word[0]
	if word[0] in upper:
		current = 'U'
	if word[0] in digit:
		current = 'D'
	if word[0] in special:
		current = 'S'
	for i in range(1, len(word)):
		if (word[i] in lower) and (current != 'A'):
			rule += current + str(i-buf)
			rulez[current + str(i-buf)][str(s)] += occ
			ruleCount[current + str(i-buf)] += occ
			buf = i
			current = 'A'
			s=''
		elif (word[i] in upper) and (current != 'U'):
			rule += current + str(i-buf)
			rulez[current + str(i-buf)][str(s)] += occ
			ruleCount[current + str(i-buf)] += occ
			buf = i
			current = 'U'
			s=''
		elif (word[i] in digit) and (current != 'D'):
			rule += current + str(i-buf)
			rulez[current + str(i-buf)][str(s)] += occ
			ruleCount[current + str(i-buf)] += occ
			buf = i
			current = 'D'
			s=''
		elif (word[i] in special) and (current != 'S'):
			rule += current + str(i-buf)
			rulez[current + str(i-buf)][str(s)] += occ
			ruleCount[current + str(i-buf)] += occ
			buf = i
			current = 'S'
			s=''
		elif len(s) >= maxnetsize:
			rule += current + str(i-buf)
			rulez[current + str(i-buf)][str(s)] += occ
			ruleCount[current + str(i-buf)] += occ
			buf = i
			s=''
		s += word[i]
	rule += current + str(len(word)-buf)
	rulez[current + str(len(word)-buf)][str(s)] += occ
	ruleCount[current + str(len(word)-buf)] += occ
	if not rule in rulez['Z']:
		rulez['Z'][rule] = 1
	rulez['Z'][rule] += occ
	ruleCount['Z'] += occ

if len(sys.argv) < 6:
	print("maxpasslength maxnetsize inputfile outputfile alterMode [genAll]")
	sys.exit()

maxpasslength = int(sys.argv[1])
maxnetsize = int(sys.argv[2])
alterMode = int(sys.argv[5])

koeficient = 100
lower = 'abcdefghijklmnopqrstuvwxyz'
upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
digit = '0123456789'
special = "+=?'~!@#$%^&*:;,.-<>`_ "
queue = deque([])
rulez = {}
rulez['Z'] = {}
ruleCount={}
if len(sys.argv) < 7:
	prepareQueue(maxpasslength,maxnetsize)
	createRules(maxnetsize)
else:
	with open(sys.argv[6]) as data_file:    
		rulez = json.load(data_file)

	for rule in rulez:
		ruleCount[rule] = len(rulez[rule])

	with open(sys.argv[3]) as f:
		for line in f:
			word = line.rstrip('\n')
			if len(word) > 0:
				w = word.split(' ', 1)
				try:
					updateMyrules(w[1], int(w[0]))
				except:
					print(w[1] + " " + w[0])
					raise
	if alterMode > 0:
		for rule in rulez:
			if (rule != 'Z'):
				for r in rulez[rule]:
					x = rulez[rule][r]
					rulez[rule][r] = float((x / ruleCount[rule]) * koeficient)

		for r in rulez['Z']:
			if (len(r) == 2):
				x = rulez['Z'][r]
				rulez['Z'][r] = float((x / ruleCount['Z']) * koeficient)

		for r in rulez['Z']:
			if (len(r) != 2):
				rulez['Z'][r] = 1
				for i in range(0, len(r), 2):
					rulez['Z'][r] *= float(rulez['Z'][r[i]+r[i+1]])
	else:
		for rule in rulez:
			for r in rulez[rule]:
				x = rulez[rule][r]
				rulez[rule][r] = float((x / ruleCount[rule]) * koeficient)

	for x in rulez:
		rulez[x] = sorted(rulez[x].items(), key=itemgetter(1), reverse=True)

with open(sys.argv[4], 'w') as fp:
    json.dump(rulez, fp, separators=(',',':'))
