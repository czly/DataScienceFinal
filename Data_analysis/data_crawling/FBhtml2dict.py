# encoding: utf-8
import sys
import lxml
from lxml import etree
import jieba

def merge_same_sentence(tmpList):
    sortList = sorted(tmpList,key=lambda d:d[0],reverse = False)
    # print(sortList)
    sortList_final = [sortList[0][:]]
    if sortList_final[0][2] == None : sortList_final[0][2]=''
    for i in range(1,len(sortList),1):
        if sortList[i][1] == sortList[i-1][1]:
            if sortList[i][2]==None: continue
            sortList_final[-1][2] += ' '+ sortList[i][2]
        else:
            sortList_final.append(sortList[i][:])
            if sortList[i][2]==None: sortList_final[-1][2] = ''
    return sortList_final



def html_to_dict(inputHtml):
    chatDict = {}
    processCount = 0
    for threadChunk in inputHtml.xpath("/html/body/div[@class='contents']/div"):
        for thread in threadChunk.findall("div"):
            # sys.stdout.write("%d,"%processCount)
            processCount+=1
            tmpList = []
            prevMinSec = [60,59]
            headers = [x for x in thread.findall("div/div")]
            msgs = [x for x in thread.findall("p")]
            for i in range(len(msgs)):
                speaker = headers[i].find("span[@class='user']").text
                timeStamp = headers[i].find("span[@class='meta']").text[:-7]
                msg = msgs[i].text
                #=====add seconds for timestamps======
                if prevMinSec[0] == int(timeStamp[-2:]):
                    if prevMinSec[1] == 0 :
                        continue
                    else :
                        prevMinSec[1] -= 1
                else :
                    prevMinSec = [int(timeStamp[-2:]),59]
                timeStamp += ":"+str(prevMinSec[1])
                #====================================
                tmpList.append([timeStamp,speaker,msg])
            tmpList = merge_same_sentence(tmpList)
            if thread.text in chatDict:
                chatDict[thread.text]['msgs'].extend(tmpList)
            else:
                chatDict[thread.text] = {'msgs':tmpList}

    return (chatDict,processCount)

def jieba_word_segmentation(chatDict,FBuser):
    for threadName in chatDict.keys():
        segDict = {}
        segListAll = []
        for msg in chatDict[threadName]['msgs']:
            if msg[2]!=None:
                segListTmp = jieba.cut(msg[2], cut_all=False,HMM=True)
            try:
                msg[2] = [i for i in segListTmp]
            except:
                msg[2] = []
            if msg[1] == FBuser:
                segListAll.extend(msg[2])
        #=====build dict=======================
        for term in segListAll:
            if term not in segDict:
                segDict[term] = 1
            else:
                segDict[term] += 1
        #======================================
        chatDict[threadName]['segm'] = segDict

def main(input_path,output_path,FBuser,should_segm=False):
    magical_parser = lxml.etree.XMLParser(encoding='utf-8', recover=True)
    inputHtml = lxml.etree.parse(input_path, magical_parser)
    (chatDict,processCount) = html_to_dict(inputHtml)
    if should_segm==True:
        jieba_word_segmentation(chatDict,FBuser)
    fout = open(output_path,"w")
    fout.write(str(chatDict))
    fout.close()
    sys.stdout.write("total processed threads:%d\n"%processCount)

if __name__ == '__main__':
    if len(sys.argv) == 4 :
        main(sys.argv[1],sys.argv[2],sys.argv[3])
    elif len(sys.argv) == 5 :
        main(sys.argv[1],sys.argv[2],sys.argv[3],True)
    else :
        print('usage:\tFBhtml2dict.py <input_file> <output_file> <FB_name> -s')
        print('example:FBhtml2dict.py yao_messages.htm yao_FBmsgDict_.txt 朱瑤章 -s')
        print('-s : optional, segment setences')
        sys.exit(0)
