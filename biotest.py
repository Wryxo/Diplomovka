from Bio import trie
from operator import itemgetter
import json

with open('TrieTest.txt', 'rb') as fp:
	a = trie.load(fp)

for x in a.keys():
	print(str(x) + ' ' + str(a[x]))
	print()