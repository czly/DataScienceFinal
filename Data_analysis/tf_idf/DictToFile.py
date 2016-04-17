import sys
import os
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

def saveFile(usrname):
    savepath = usrname + "_text/"
    if not os.path.exists("./" + usrname + "_text/"):
        os.mkdir(usrname + "_text")
        print("mkdir: ./" + usrname + "_text/ ...")
    file_list = []
    f1 = open(usrname + "_msgDict.txt", "r")
    content = f1.read()
    dictUsr = eval(content) #turn str -> dict object

    print("saving files into ./" + usrname + "_text/ ...")
    idx = 0
    for item in dictUsr:
        filename = savepath + str(idx)
        
        print("key: " + str(item) + ", saving " + filename)
        file_out = open(filename, "a")
        file_out.write(str(item) + '\n')
        file_out.write(str(len(dictUsr[item]['msgs'])) + '\n')
        for key in dictUsr[item]['segm']:
            for i in range(int(dictUsr[item]['segm'][key])):
                file_out.write(str(key) + ' ')
        file_out.close()

        idx += 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage:\tpython DictToFile.py <username>")
        print("username should be YAO, CHL, CWH or JN")
    else:
        saveFile(sys.argv[1])
