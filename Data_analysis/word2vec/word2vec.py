import jieba
import gensim
import sys

sentence = []
for line in open(sys.argv[1]):
	temp = []
	temp += jieba.cut(line, cut_all=False)
	sentence.append(temp)

model = gensim.models.Word2Vec(sentence, size=300, min_count=1, workers=4)
model.save(sys.argv[2])


print (model.similarity('男孩', '女孩'))
print (model.most_similar(positive=['男孩', '魯蛇'], negative=['女孩']))
