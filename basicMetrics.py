import sys
try:
    from Bio import trie
except ImportError:
    import os
    from Bio import MissingExternalDependencyError
    if os.name=="java":
        message = "Not available on Jython, Bio.trie requires compiled C code."
    else:
        message = "Could not import Bio.trie, check C code was compiled."
    raise MissingExternalDependencyError(message)

d = trie.trie()
marked = []
c = 0
cc = 0
sooner = 0
later = 0
total = 0

with open(sys.argv[1]) as data_file:    
	for line in data_file:
		d[line[:-1]] = c
		c += 1

with open(sys.argv[2]) as data_file:    
	for line in data_file:
		if line[:-1] in d:
			total += d[line[:-1]] - cc
		else:
			total += cc
		cc += 1
		
print(len(d))
print(str(total) + ' ' + str(cc) + ' ' + str(c))
print(total / cc)
