# encoding: utf-8
import sys
import lxml
from lxml import etree
import jieba

def main(input_path,output_path,FBuser):
    magical_parser = lxml.etree.XMLParser(encoding='utf-8', recover=True)
    inputHtml = lxml.etree.parse(input_path, magical_parser)

    chatDict = {}
    processCount = 0

    #=====html to dict=====================================
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
            if thread.text in chatDict:
                chatDict[thread.text]['msgs'].extend(tmpList)
            else:
                chatDict[thread.text] = {'msgs':tmpList}
    #======================================================
    #=====jieba word segmentation==========================
    for threadName in chatDict.keys():
        segDict = {}
        msgstrs = ""
        for msg in chatDict[threadName]['msgs']:
            if msg[1] == FBuser:
                try:
                    msgstrs += ','+msg[2]
                except:
                    pass
        #=====segment==========================
        segList = jieba.cut(msgstrs, cut_all=False,HMM=True)
        #======================================
        #=====build dict=======================
        for term in segList:
            if term not in segDict:
                segDict[term] = 1
            else:
                segDict[term] += 1
        #======================================
        chatDict[threadName]['segm'] = segDict
    #======================================================
    fout = open(output_path,"w")
    fout.write(str(chatDict))
    fout.close()
    sys.stdout.write("total processed threads:%d\n"%processCount)

if __name__ == '__main__':
    if len(sys.argv) == 4:
        # FBname = input("input your Facebook name:\nex:朱瑤章")
        main(sys.argv[1],sys.argv[2],sys.argv[3])
    else :
        print('usage:\tFBhtml2dict.py <input_file> <output_file> <FB_name>')
        print('example:FBhtml2dict.py yao_messages.htm yao_FBmsgDict_.txt 朱瑤章')
        sys.exit(0)
