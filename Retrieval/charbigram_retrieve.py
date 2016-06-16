from Base import BaseRetrieve
import re
import numpy as np
import sys
from gensim.matutils import unitvec
import gensim
from gensim.models.doc2vec import TaggedDocument ,Doc2Vec
from random import shuffle
class CharbigramRetrieve(BaseRetrieve):
    def __init__(self,dataset,
                 nss=set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')):
        '''
            input : dataset=filepath or [filepath1,filepath2,...] , all the chatbox file to input
                    nss=set of characters which should not be split in bigram
            This step will preprocessing , build the data for training.
            
            
            self.not_split_set : same as input nss , default is all English alphabet and number
            self.msg_dict : original input msg dict , ex: {['人1','人2'] = ['msg':[...]],...}
            self.msg_sents : list of all the sentences in msg_dict , ex: ['對話1','對話2','對話3']
            self.qmapa : query index map answer , input sent's id map to next sent as reply
                                  ex: ['你好','你也是!'] => qmapa[0] = '你也是!'
            self.lbigram : bigram version of msg_sents
            self.model : Doc2vec model
            
            
            easy usage : >> cbg = charbigram_Retrieve("YAO_dict")
                         >> cbg.train_Doc2vec()
                         >> cbg.get_similar_sents("要不要出去念書?")
                         >> cbg.get_response("中午要吃什麼")
                         >> with open('model1','wb') as f1:    pickle.dump(cbg,f1) #save model
                         >> with open('model1','rb') as f1:    cbg = pickle.load(f1) #load model
        '''
        super(BaseRetrieve,self).__init__()
        self.not_split_set = nss
        self.msg_dict = dict()  #original msg dict
        self.msg_sents = [] #list of sentences
        self.qmapa = dict()  #query map answer
        self.lbigram = []
        self.model = None
        
        #load multiple chatbox or one
        if type(dataset) == list:
            for data in dataset:
                with open(data,'r') as f1:
                    self.msg_dict.update(eval(f1.read()))
        else:
            with open(dataset,'r') as f1:
                self.msg_dict = eval(f1.read())
        
        #preprocessing , make qmapa and msg_sents
        r1 = re.compile('[^\u4e00-\u9fffA-z0-9]|[_\^]',re.U) #match all not-chinese characters
        r2 = re.compile(' +') #match blank num >= 1
        count = 0
        for k in self.msg_dict.keys():
            thread1 = self.msg_dict[k]['msgs']
            len_thread1 = len(thread1)
            self.msg_sents.append((r2.sub(' ',r1.sub(" ",thread1[0][2]))).strip())
            count+=1
            for i in range(1,len_thread1,1):
                self.msg_sents.append((r2.sub(' ',r1.sub(" ",thread1[i][2]))).strip())
                self.qmapa[count-1] = self.msg_sents[-1]
                count+=1
        
        #make bigram list for all sentences
        for msg in self.msg_sents:
            tmp = msg.split(' ')
            while '' in tmp:
                del tmp[tmp.index('')]
            ltmp = []
            for i in tmp:
                ltmp.extend(self.make_bigram(i))
            self.lbigram.append(ltmp[:])
        for bi in self.lbigram:
            if len(bi) == 0:
                bi.append('<None>')

    def make_bigram(self,strin):
        '''
            input : str for making bigram
            output: list of str of bigram
        '''
        lstrin = list(strin)
        ltmp = ['<s>',lstrin[0]]
        for i in range(1,len(lstrin),1):
            if lstrin[i] in self.not_split_set:
                if lstrin[i-1] in self.not_split_set:  ltmp[-1]+=lstrin[i]
                else:  ltmp.append(lstrin[i])
            else:
                ltmp.append(lstrin[i])
        ltmp.append('<e>')
        lbigram = []
        for i in range(len(ltmp)-1):
            lbigram.append(ltmp[i]+ltmp[i+1])
        return lbigram
    def train_Doc2vec(self,sent_num=None,iter_num=10,shuf=True):
        '''
            input : sent_num = int, number of sentences want to train
                    iter_num = int, number of iteration doc2vec will train
                    shuf = bool , if want to shuffle sentences list every training epoch
                    
            other parameters is tune by me
        '''
        sentences= [TaggedDocument(self.lbigram[i], [i]) for i in range(len(self.lbigram))]
        if sent_num != None:
            sentences = sentences[:sent_num]
        
        self.model = Doc2Vec(size=200, alpha=0.025,min_alpha=0.025,workers=4, min_count=1, dm=0)  # use fixed learning rate
        self.model.build_vocab(sentences)
        print("now running Doc2vec training iteration:")
        for epoch in range(iter_num):
            sys.stdout.write("%d,"%epoch)
            if shuf==True:
                shuffle(sentences)
            self.model.train(sentences)
            self.model.alpha -= 0.002  # decrease the learning rate
            self.model.min_alpha = self.model.alpha
    def get_similar_sents(self,strin,topk=10):
        '''
            input : str , sentence want to ask . ex: '今天過的如何?'
            output: list of (similarity,str) , top k sentence similar to input str.
        '''
        sim_list = dict()
        v1 = self.model.infer_vector(self.make_bigram(strin))
        for i in range(self.model.docvecs.count):
            sim_list[np.dot(unitvec(v1),unitvec(self.model.docvecs[i]))] = self.msg_sents[i]
        return sorted(sim_list.items(),key=lambda k:k[0],reverse=True)[:topk]
    def get_response(self,strin,topk=10):
        '''
            input : str , sentence want to ask . ex: '今天過的如何?'
            output: list of (similarity,str) , top k sentence replied by sentences most similar to input str.
        '''
        res_list = dict()
        v1 = self.model.infer_vector(self.make_bigram(strin))
        for i in range(self.model.docvecs.count):
            tmp = self.qmapa[i] if (i in self.qmapa) else self.msg_sents[i]
            res_list[np.dot(unitvec(v1),unitvec(self.model.docvecs[i]))] = tmp
        return sorted(res_list.items(),key=lambda k:k[0],reverse=True)[:topk]