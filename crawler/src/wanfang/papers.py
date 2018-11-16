# coding=utf-8
# date:下午2:51 
# author:chenjunbiao

import requests
import time
import re
import os
from bs4 import BeautifulSoup
import bs4
from multiprocessing import Pool
import xlwt


def get_html(url):
    try:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.90 Safari/537.36 2345Explorer/9.3.2.17331', }
        r = requests.get(url, headers=header, verify=False)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        # print(r.text)
        return r
    except Exception as e:
        print("has error:" + str(e))


def getNum(key):
    head = "http://www.wanfangdata.com.cn/search/searchList.do?searchType=degree&showType=&searchWord="
    end = "&isTriggerTag="
    url = head + key + end
    # re1 = r'\s*找到<strong>(.*?)</strong>条结果'
    re1 = r'\s*找到 <span>(.*?)</span> 条结果'
    html = get_html(url).text
    if html == None:
        print("没有文献")
        return
    bs = BeautifulSoup(html, 'html.parser')
    strnum = bs.select('.BatchOper_result_show span')[0].text
    # strnum = re.findall(re1, html)
    num = int(strnum)
    # print("找到了：",num)
    return num


def search_key(key):
    allurl = []
    page = 0
    head = "http://www.wanfangdata.com.cn/search/searchList.do?searchType=all&showType=&searchWord="
    end = "&isTriggerTag="
    url = head + key + end
    # print(url)
    allurl.append(url)
    html = get_html(url).text
    if html == None:
        print("text empty")
        return
    num = getNum(key)
    print("找到了：", num)
    if num > 20:
        if num % 20 != 0:
            page = num // 20 + 1
        else:
            page = num // 20
    # page>1 url
    head = 'http://www.wanfangdata.com.cn/search/searchList.do?searchType=degree&pageSize=20&page='
    end = '&searchWord=' + key + '&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&firstAuthor=false&rangeParame=all'
    for i in range(2, page + 1):
        url = head + str(i) + end
        allurl.append(url)
    l = len(allurl)
    print('第', l, "页")
    print(allurl[0])
    print(allurl[l - 1])
    return allurl


def get_url(urls):
    base = 'http://www.wanfangdata.com.cn//link.do'
    html = get_html(urls).text
    # re0=r'<a href="(.*?)">'
    re0 = r'<a\b[^>]*\bhref="/link.do?([^"]+)'
    allUrl = re.findall(re0, html)
    length = len(allUrl)
    print("length=", length)
    for i in range(length):
        allUrl[i] = base + allUrl[i]
        # print(allUrl)
    return allUrl


# def getdownurl(url):
#     text = get_html(url).text
#     re0 = r'<a onclick="upload\((.*?)\)"'
#     firurl = re.findall(re0, text)
#     print(firurl)
#     if len(firurl) == 0:
#         return
#     strurl = str(firurl[0])
#     print(strurl)
#     tpurl = re.split(',', strurl)
#     endstp = []
#     # print(tpurl)
#     for ul in tpurl:
#         elem = ul.strip('\'').strip('\'')
#         endstp.append(elem)
#     print(endstp, type(endstp[0]))
#     head = 'http://www.wanfangdata.com.cn/search/downLoad.do?page_cnt='
#     geturl = head + endstp[0] + "&language=" + endstp[2] + "&resourceType=" + endstp[6] + "&source=" + endstp[
#         3] + "&resourceId=" + endstp[1] + "&resourceTitle=" + endstp[4] + "&isoa=" + endstp[5] + "&type=" + endstp[0]
#     print(geturl)
#     re1 = r'<iframe style="display:none" id="downloadIframe" src="(.*?)">'
#     text = get_html(geturl).text
#     print()
#     sucurl = re.findall(re1, text)
#     print(sucurl)
#     return sucurl[0]


def get_pdf(url, title):
    text = get_html(url)
    path = "/home/dflx/下载/万方数据库/深度学习/" + title + ".pdf"
    with open(path, 'wb') as f:
        f.write(text.content)
    print("successf")


def getdownurl(url):
    text = get_html(url).text
    re0 = r'<a onclick="upload\((.*?)\)"'
    firurl = re.findall(re0, text)
    print(firurl)
    if len(firurl) == 0:
        return
    strurl = str(firurl[0])
    print(strurl)
    tpurl = re.split(',', strurl)
    endstp = []
    # print(tpurl)
    for ul in tpurl:
        elem = ul.strip('\'').strip('\'')
        endstp.append(elem)
    print(endstp, type(endstp[0]))
    head = 'http://www.wanfangdata.com.cn/search/downLoad.do?page_cnt='
    geturl = head + endstp[0] + "&language=" + endstp[2] + "&resourceType=" + endstp[6] + "&source=" + endstp[
        3] + "&resourceId=" + endstp[1] + "&resourceTitle=" + endstp[4] + "&isoa=" + endstp[5] + "&type=" + endstp[0]
    print(geturl)
    re1 = r'<iframe style="display:none" id="downloadIframe" src="(.*?)">'
    text = get_html(geturl).text
    print()
    sucurl = re.findall(re1, text)
    print(sucurl)
    return sucurl[0]


def downloadAllPdf(key):
    # row=getNum(key)
    pages = search_key(key)
    allurl = []
    num = 0
    for page in pages:
        allurl = get_url(page)
        for url in allurl:
            # 得到每一篇文献的信息，写入文件
            num += 1

            re0 = r'<title>(.*?)</title>'
            text = get_html(url).text
            title = re.findall(re0, text)[0]
            print("下载：", title)
            geturl = getdownurl(url)
            get_pdf(geturl, title)
            print("all downloads is", num)
            # try:
            #     re0 = r'<title>(.*?)</title>'
            #     text = get_html(url).text
            #     title = re.findall(re0, text)[0]
            #     print("下载：", title)
            #     geturl = getdownurl(url)
            #     get_pdf(geturl, title)
            # except BaseException as e:
            #     print("has except")
            #     print(e)
            #     continue
            # finally:
            #     print("all downloads is", num)


def main():
    with open(r'2018-11-16下午4-4-37@WanFangdata.txt', 'r') as f:
        paper_titles = f.readlines()
    for line in paper_titles:
        if len(line) > 5:
            title = line.lstrip('【篇名】').strip()
            downloadAllPdf(title)


if __name__ == '__main__':
    main()
