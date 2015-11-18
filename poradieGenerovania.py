a = [200, 91, 82]
b = [22, 20, 18, 9, 7]
res = []
for i in range(0,3):
	for j in range(0,3):
		for k in range(0,5):
			res.append((i,j,k,a[i]*a[j]*b[k]))
tres = sorted(res, key=lambda x: x[3], reverse=True)
print(tres)