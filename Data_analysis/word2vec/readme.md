word2vec.py:
依照目標檔案中的字句train出一個空間，使其每個詞彙都代表一個向量

需求：
python3(若目標檔案內容為中文)
jieba(斷詞工具，若目標檔案內容為中文)
gensim(word2vector套件)

使用方法：
python3 word2vec.py "目標檔案路徑" "欲將生成的model寫入的路徑"


Dcardvocablist.py:
建出Dcard上有出現過的詞彙

需求：
python3
jieba

使用方法：
python3 Dcardvocablist.py "文檔路徑" "輸出詞彙檔的路徑"


cluster.py:
針對某個聊天記錄分類出相同聊天模式的聊天框

需求：
python3
sklearn
gensim
numpy
matplotlib

使用方法：
python3 cluster.py "word2vector model路徑" "聊天記錄路徑" "word2vector的vocablist" "空白檔"
