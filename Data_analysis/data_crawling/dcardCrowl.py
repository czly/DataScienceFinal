import requests
import json
import time
import sys

def main(from_postid,to_postid,output_path):
	f11 = open(output_path,"a")
	count = 0
	print("now has crowled:")
	for postID in range(from_postid,to_postid):   #10001 ~ 1000000
	    res2 = requests.get("https://www.dcard.tw/api/post/all/%d"%postID)
	    s2 = json.loads(res2.text)
	    time.sleep(0.1)
	    count += 1
	    if count%100==0 :
	        sys.stdout.write("%d,"%count)
	    try:
	        f11.write(s2['version'][0]['content']+'\n')
	        for comment in s2['comment']:
	            f11.write(comment['version'][0]['content']+'\n')
	    except:
	        continue
	f11.close()

if __name__ == '__main__':
    if len(sys.argv) == 4:
        main(int(sys.argv[1]),int(sys.argv[2]),sys.argv[3])
    else :
        print('usage:\tdcardCrowl.py <from_postid> <to_postid> <output_file>')
        print('example:dcardCrowl.py 10001 1000000 dcardData.txt')
        sys.exit(0)