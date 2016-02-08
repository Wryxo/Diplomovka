from itertools import *
from operator import itemgetter
from collections import deque
import heapq
import copy
import json
import sys


if len(sys.argv) < 3:
	print("wordCount inputfile")
	sys.exit()

with open(sys.argv[2]) as data_file:    
    rulez = json.load(data_file)

pq = []
counter = count()
maximum = int(sys.argv[1])
c = 0

def add_task(task, priority=0):
    count = next(counter)
    entry = [-priority, count, task]
    heapq.heappush(pq, entry)

def pop_task():
	priority, count, task = heapq.heappop(pq)
	return -priority, task

nt = rulez['Z'][0]
fp = nt[1]
for i in range(0, len(nt[0])//2):
	fp = fp * rulez[nt[0][i*2:(i+1)*2]][0][1]
add_task((0, [0] + ([0]*(len(nt[0])//2))), fp)

while pq:
	c += 1
	priority, task = pop_task()
	if c > maximum:
		break
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
				