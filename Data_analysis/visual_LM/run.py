import LM
import pickle as pkl
import Visual_tools as vt
import matplotlib.pyplot as plot

if __name__ == '__main__':
    fb_dict = LM.fb_file_to_dict('../../Data/FB/JN_msgDict.txt')
    new_dict = LM.filter_outlier(fb_dict, threshold=200)
    all_LMs = LM.build_all_chat_LM(new_dict, max_len=2)
    

    dissimilarity, ID_map = LM.export_dissimilarity(all_LMs)
    plot.matshow(dissimilarity)
    plot.colorbar()
    plot.show()
    pkl.dump(ID_map, open('./ID_map.pkl', 'w'))

    pos, plt = vt.visual_mds(dissimilarity)
    plt.show()

