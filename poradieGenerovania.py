a = [200, 91, 82]
b = [22, 20, 18, 9, 7]
c = [47, 45, 42, 27, 11]
res = []
for i in range(0,3):
	for j in range(0,5):
		for k in range(0,5):
			res.append((i,j,k,a[i]*b[j]*c[k]))
tres = sorted(res, key=lambda x: x[3], reverse=True)
for z in tres:
	print(z)
x = [0, 0, 0]

#while x[0]<len(a)-1 and x[1]<len(a)-1 and x[2]<len(b)-1:
	#print(a[x[0]]*a[x[0]]*a[x[0]] + " " + str(x))