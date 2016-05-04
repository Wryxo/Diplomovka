from itertools import *
from operator import itemgetter
from collections import deque
from memory_profiler import profile
import heapq
import copy
import json
import sys
import os.path


def add_task(task, priority=0):
    count = next(counter)
    entry = [-priority, count, task]
    heapq.heappush(pq, entry)

def pop_task():
	priority, count, task = heapq.heappop(pq)
	return -priority, task

@profile
def generateWords(maximum):
	c = 0
	while pq:
		c += 1
		if c > maximum:
			break
		priority, task = pop_task()
		net = rulez['Z'][task[1][0]][0]
		out = ''
		for x in range(1,len(task[1])):
			out += rulez[net[(x-1)*2:x*2]][task[1][x]][0]
		print(out)
		if task[0] == 0:
			if task[1][0]+1 >= len(rulez['Z']):
				continue
			nnet = rulez['Z'][task[1][0]+1]
			newpriority = nnet[1]
			for i in range(0, len(nnet[0])//2):
				newpriority = newpriority * rulez[nnet[0][i*2:(i+1)*2]][0][1]
			add_task((0, [task[1][0]+1] + ([0]*(len(nnet[0])//2))), newpriority)
			for x in range(1,len(task[1])):
				tmp = copy.deepcopy(task[1])
				newpriority = priority / rulez[net[(x-1)*2:x*2]][tmp[x]][1]
				tmp[x] += 1
				if tmp[x] >= len(rulez[net[(x-1)*2:x*2]]):
					continue
				newpriority = newpriority * rulez[net[(x-1)*2:x*2]][tmp[x]][1]
				newtask = (x, tmp)
				add_task(newtask, newpriority)
		else:
			for x in range(task[0],len(task[1])):
				tmp = copy.deepcopy(task[1])
				newpriority = priority / rulez[net[(x-1)*2:x*2]][tmp[x]][1]
				tmp[x] += 1
				if tmp[x] >= len(rulez[net[(x-1)*2:x*2]]):
					continue
				newpriority = newpriority * rulez[net[(x-1)*2:x*2]][tmp[x]][1]
				newtask = (x, tmp)
				add_task(newtask, newpriority)

@profile
def loadGrammar():
	with open(sys.argv[2]) as data_file:    
		return json.load(data_file)

if len(sys.argv) < 3:
	print("wordCount grammarFile")
	sys.exit()

cont = 'x'
if (os.path.isfile(sys.argv[2]+'.ls')):
	print("Session for this grammar found, continue ? y/n", file=sys.stderr)
	while cont != 'n' and cont != 'y': 
		cont = sys.stdin.read(1)

pq = []
counter = count()
maximum = int(sys.argv[1])
rulez = loadGrammar()

if (cont == 'y'):
	with open(sys.argv[2]+'.ls') as data_file:    
		pq = json.load(data_file)
	m = max(pq)
	counter = count(m[1]+1)
else:
	nt = rulez['Z'][0]
	fp = nt[1]
	for i in range(0, len(nt[0])//2):
		fp = fp * rulez[nt[0][i*2:(i+1)*2]][0][1]
	add_task((0, [0] + ([0]*(len(nt[0])//2))), fp)
try:
	generateWords(maximum)
	with open(sys.argv[2]+'.ls', 'w') as outfile:
		json.dump(pq, outfile, separators=(',',':'))
	print('Session saved', file=sys.stderr)
	sys.exit(0)
except KeyboardInterrupt:
	add_task(task, priority)
	with open(sys.argv[2]+'.ls', 'w') as outfile:
		json.dump(pq, outfile, separators=(',',':'))
	print('Session saved', file=sys.stderr)
	sys.exit(0)

