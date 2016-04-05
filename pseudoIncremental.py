from collections import deque
import sys

if len(sys.argv) < 4:
	print("maxlength inputfile outputfile")
	sys.exit()

abeceda = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+=?'~!@#$%^&*:;,.-<>`_"
odds = {}
maxlength = int(sys.argv[1])

for x in abeceda:
	odds[x] = 0

with open(sys.argv[2]) as f:
	for line in f:
		for x in line:
			if x in abeceda:
				odds[x] += 1

odds = sorted(odds, key=lambda key: odds[key], reverse=True)
queue = deque(odds)
finished = False
with open(sys.argv[3], 'w') as ofile:
	while queue:
		tmp = queue.popleft()
		for x in abeceda:
			a = tmp + x
			if len(a) > maxlength:
				finished = True
				break
			queue.append(a)
			
		if finished:
			break
		ofile.write(tmp+'\n')