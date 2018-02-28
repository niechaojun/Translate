#coding=utf8
import requests as rs
import md5
import random
import json
import re
import chardet
import sys
import os

log = []

def N_trans(q,fromLang,toLang):
    global log
    appid = '20180129000119577'
    secretKey = 'P_tuYcSWGzer6nFRRic9'
    myurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()
    url = myurl + '?appid=' + appid + '&q=' + q + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign
    try:
        try:
            r1 = rs.get(url,timeout=5).text
        except:
            print u"网络超时,无法进行在线翻译"
            exit(1)
        in_json = json.loads(r1)
        # print in_json
        print
        result = q.decode('utf-8')+" : "+in_json['trans_result'][0]['dst']
        print u"在线翻译 ： "+result
        for log1 in log:
            if(result==log[0].strip('\n').decode('utf-8')):
                exit(1)
        fp = open(os.getcwd()+os.sep+"log\\translate.log", 'a+')
        fp.write(q+" : " + in_json['trans_result'][0]['dst'].encode('utf-8')+'\n')
        fp.close()
    except Exception, e:
        print e

def N_Checklog(q):
    global log
    if os.path.exists(os.getcwd()+os.sep+"log\\translate.log"):
        fp = open(os.getcwd()+os.sep+"log\\translate.log",'r')
        for i in fp.readlines():
            if q in i:
                print i.strip('\n').decode('utf-8')
                log.append(i)
        fp.close()

if __name__=='__main__':
    print
    try:
        q= sys.argv[1].decode('gbk').encode('utf-8')
    except:
        print u"example：python Nienie_Translate \"你好\""
        exit(0)
    #print chardet.detect(q)['encoding']
    if chardet.detect(q)['encoding'] == 'ascii':
        fromLang = 'en'
        toLang = 'zh'
    else:
        fromLang = 'zh'
        toLang = 'en'
    N_Checklog(q)
    N_trans(q, fromLang, toLang)


