import gensim
import sklearn
import numpy as np
import math
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import sys

def vectordistance(A,B):
	C = A-B
	score = 0.0
	for i in range(len(C)):
		score += pow(C[i],2)
	return math.sqrt(score)


model = gensim.models.Word2Vec.load(sys.argv[1])

#read data from tf-idf
datauncount = []
temp = []
for line in open(sys.argv[2]):
	if line[0] != '[':
		if len(temp) > 1 and len(temp[0]) > 1 and int(temp[0][-1]) > 500 and len(temp[0]) < 4:
			datauncount.append(temp)
		temp = []
		name = line.strip().split(',')
		for i in range(1,len(name)):
			if i == len(name)-1:
				name.append(name[i].split(' ')[-1])
			if len(name[i].split(' ')) < 4 :
				name[i] = name[i].split(' ')[1]
		temp.append(name)
	else:
		line = line.strip().split('[')[1].split(']')[0].split(',')
		line[0] = line[0].split('\'')[1]
		line[1] = line[1].split(' ')[1]
		temp.append(line)


#read data from vocablist
vocab_set = set()
for word in open(sys.argv[3]):
	vocab_set.add(word)
for word in open(sys.argv[4]):
	vocab_set.remove(word)

print (len(datauncount))

#normalize vector
datavector = []
a = 0
for i in range(len(datauncount)):
	count = 0.0
	for j in range(1,len(datauncount[i])):
		if(str(datauncount[i][j][0]+'\n') in vocab_set):
			if count == 0:
				try:
					temp = model[datauncount[i][j][0]]*float(datauncount[i][j][1])
					count += float(datauncount[i][j][1])
				except KeyError:
					with open(sys.argv[4],"a") as f:
						f.write(str(datauncount[i][j][0])+'\n')
					vocab_set.remove(str(datauncount[i][j][0])+'\n')
			else:
				try:
					temp += model[datauncount[i][j][0]]*float(datauncount[i][j][1])
					count += float(datauncount[i][j][1])
				except KeyError:
					with open(sys.argv[4],"a") as f:
						f.write(str(datauncount[i][j][0])+'\n')
					vocab_set.remove(str(datauncount[i][j][0])+'\n')
	temp /= count
	datavector.append(temp)

dataset = []
for i in range(len(datavector)):
	temp = []
	for j in range(len(datavector)):
		temp.append(np.inner(datavector[i],datavector[j]))
	dataset.append(temp)


kmeans = KMeans(n_jobs = 2, n_clusters=15)

reduced_data = PCA(n_components=2).fit_transform(dataset)
kmeans.fit(reduced_data)
h = .02
x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

# Obtain labels for each point in mesh. Use last trained model.
Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

# Put the result into a color plot
Z = Z.reshape(xx.shape)
plt.figure(1)
plt.clf()
plt.imshow(Z, interpolation='nearest',
           extent=(xx.min(), xx.max(), yy.min(), yy.max()),
           cmap=plt.cm.Paired,
           aspect='auto', origin='lower')

plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
# Plot the centroids as a white X
centroids = kmeans.cluster_centers_
plt.scatter(centroids[:, 0], centroids[:, 1],
            marker='x', s=169, linewidths=3,
            color='w', zorder=10)
plt.title('K-means clustering on the digits dataset (PCA-reduced data)\n'
          'Centroids are marked with white cross')
for i in range(len(datauncount)):
	if (datauncount[i][0][0] == '李承軒'):
		datauncount[i][0][0],datauncount[i][0][1] = datauncount[i][0][1],datauncount[i][0][0]
	if (ord(datauncount[i][0][0][-1]) - ord('0') < 10 and ord(datauncount[i][0][0][-1]) - ord('0') >= 0):
		temp = ''
		for j in range(1,len(datauncount[i][0][0].split(' '))-1):
			temp += str(datauncount[i][0][0].split(' ')[j])
		datauncount[i][0][0] = temp
for i in range(len(reduced_data)):
	plt.annotate(datauncount[i][0][0],(reduced_data[:,0][i],reduced_data[:, 1][i]))

plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.xticks(())
plt.yticks(())
ans = kmeans.predict(reduced_data)
for i in range(len(ans)):
	print (datauncount[i][0],ans[i])

plt.show()
