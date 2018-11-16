# -*- coding: utf-8 -*-
# @Time    : 17-7-18 下午2:25
# @Author  : stephenfeng
# @Software: PyCharm Community Edition
import random

'''
浏览器的报文头
'''

useragent_phonelist = [
    'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Mobile Safari/537.36', \
    'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Mobile Safari/537.36', \
    'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Mobile Safari/537.36', \
    'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1', \
    'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1']

useragent_pclist = [
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36', \
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0', \
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.32', \
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36', \
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586', \
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko', \
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.3 Safari/537.36', \
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.9.2.1000 Chrome/39.0.2146.0 Safari/537.36', \
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.277.400 QQBrowser/9.4.7658.400', \
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 UBrowser/5.6.12150.8 Safari/537.36', \
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0', \
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.154 Safari/537.36 LBBROWSER ', \
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36 TheWorld 7' \
    ]

# 要加入'User-Agent'
headers = {'Accept': 'application/json, text/plain, */*', \
           'Accept-Encoding': 'gzip, deflate', \
           'Accept-Language': 'zh-CN,zh;q=0.8', \
           'Cache-Control': 'no-cache', \
           'Connection': 'keep-alive', \
           'Host': 'm.weibo.cn',
           'X-Requested-With': 'XMLHttpRequest'
           # 'Cookie': 'wvr=6; _s_tentry=www.weibo.com; UOR=www.weibo.com,d.weibo.com,spr_sinamkt_buy_hyww_weibo_t112; Apache=5480829615959.64.1500466223405; SINAGLOBAL=5480829615959.64.1500466223405; ULV=1500466223431:1:1:1:5480829615959.64.1500466223405:; TC-Page-G0=cdcf495cbaea129529aa606e7629fea7; TC-Ugrow-G0=5e22903358df63c5e3fd2c757419b456; TC-V5-G0=10672b10b3abf31f7349754fca5d2248; SCF=AlH2RAscUrE4I5lPkjxc1vhAfign5scXe-JToJGdC8se71U_pq7bDqGkUnuUfEcKqfnbfKgHN_fn_rRi_sppkeQ.; SUB=_2A250dekcDeRhGeBN6lUU8SrMzTSIHXVXA13UrDV8PUJbmtAKLUXQkW9oUJ19Vify2ANIZ7my1sQx-R2x5Q..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFpZ_PcW5cM8ak0qLTUZTV65JpX5o2p5NHD95Qce02NSK2XehqRWs4DqcjJi--4iKnNiKysi--Ri-8siKy2i--fiKysiKyhi--ciKL2i-279Lqt; SUHB=0vJI5Q4vDPfQY0'
           }


def choose_ua(client='pc'):
    agentList = useragent_phonelist if client != 'pc' else useragent_pclist
    ua = random.choice(agentList)
    return ua
