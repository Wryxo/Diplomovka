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