import sys
import os
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

def saveFile(usrname):
    savepath = usrname + "_text/"
    if not os.path.exists("./" + usrname + "_text/"):
        os.mkdir(usrname + "_text")
    file_list = []
    f1 = open(usrname + "_msgDict.txt", "r")
    s1 = ""
    for line in f1:
        s1 += line
    dictYao = eval(s1) #turn str -> dict object

    for item in dictYao:
        filename = ""
        if len(savepath + str(item)) > 20:
            filename = savepath + "group"
        else:
            filename = savepath + str(item)

        file_list.append(filename)
        file_out = open(filename, "w")
        for key in dictYao[item]['segm']:
            for i in range(int(dictYao[item]['segm'][key])):
                file_out.write(str(key) + ' ')
        file_out.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage:\tpython DictToFile.py <username>")
        print("username should be YAO, CHL, CWH or JN")
    else:
        saveFile(sys.argv[1])
