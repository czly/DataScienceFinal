from sklearn import manifold
import matplotlib.pyplot as plt
import pickle as pkl

def visual_mds(dissimilarity):
	mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9, dissimilarity='precomputed')
	pos = mds.fit(dissimilarity).embedding_
	plt.scatter(pos[:, 0], pos[:, 1], c='b')
	pkl.dump(pos, open('pos.pkl', 'w'))
	return pos, plt
	# plt.show()

def visual_nmds(dissimilarity):
	nmds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-12, dissimilarity='precomputed', metric=False)
	pass

def search(xm, xM, ym, yM, pos, ID_map):
	ret = []
	for idx, p in enumerate(pos):
		if p[0] > xm and p[0] < xM and p[1] > ym and p[1] < yM:
			print '* '+ID_map[idx]
			ret.append(ID_map[idx])

	return ret