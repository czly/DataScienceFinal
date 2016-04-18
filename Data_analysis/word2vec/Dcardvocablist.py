import jieba
import sys

vocab_set = set()
a = 0
for line in open(sys.argv[1]):
	if a % 10000 == 0:
		print (a)
	for word in jieba.cut(line, cut_all=False): 
		vocab_set.add(word)
	a += 1


with open(sys.argv[2],'w') as f:
	for word in vocab_set:
		f.write(word+'\n')
