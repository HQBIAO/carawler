# coding=utf-8
# date:下午2:51 
# author:chenjunbiao
import json

import requests
import re
from bs4 import BeautifulSoup

from crawler.src.wiki.utilAgent import choose_ua


def get_html(url):
    try:
        header = {
            'User-Agent': choose_ua(),
            'Cookie': 'cnkiUserKey=00bc73d9-a156-e26e-77c3-42929cb28067; Ecp_ClientId=2180402145004264272; UM_distinctid=166ab1b02841b5-0d1dff9ad08ac4-346a7808-1fa400-166ab1b0285577; SID_search=201087; Ecp_session=1; ASP.NET_SessionId=3icyxccmo3ykdovyqbauqqns; SID_sug=111055; LID=WEEvREcwSlJHSldRa1FhdkJkVWEyd1JiUDgrRnBQUmNZcVI3d0V6YVBrMD0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!; Ecp_LoginStuts=%7B%22IsAutoLogin%22%3Afalse%2C%22UserName%22%3A%22GDJNDX%22%2C%22ShowName%22%3A%22%25E6%259A%25A8%25E5%258D%2597%25E5%25A4%25A7%25E5%25AD%25A6%22%2C%22UserType%22%3A%22bk%22%2C%22r%22%3A%22CbxUQn%22%7D; c_m_LinID=LinID=WEEvREcwSlJHSldRa1FhdkJkVWEyd1JiUDgrRnBQUmNZcVI3d0V6YVBrMD0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!&ot=12/14/2018 18:14:00; c_m_expire=2018-12-14 18:14:00'}
        r = requests.get(url, headers=header, verify=False)
        r.encoding = r.apparent_encoding
        # print(r.text)
        return r
    except Exception as e:
        print("has error:" + str(e))
        return None


def getNum(key):
    head = "http://www.wanfangdata.com.cn/search/searchList.do?searchType=degree&showType=&searchWord="
    end = "&isTriggerTag="
    url = head + key + end
    html = get_html(url).text
    bs = BeautifulSoup(html, 'html.parser')
    el = bs.select('.BatchOper_result_show span')
    strnum = el[0].text if el else 0
    num = int(strnum)
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
    print("找到了关于标题 '" + key + "'： 的文章篇数为：", num)
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


def get_pdf(url, title, page=0):
    text = get_html(url)
    # path = "/Users/chenjunbiao/project/carawler/crawler/src/wanfang/data/" + title + ".pdf"
    path = "/home/zengchuan/wanfang/" + str(page) + "/" + title + ".pdf"
    with open(path, 'wb') as f:
        f.write(text.content)
    print("successf")


def download_pdf(source_url, save_path):
    """
    下载pdf文件
    :param source_url:
    :param save_path:
    :return:
    """
    text = get_html(source_url)
    with open(save_path, 'wb') as f:
        f.write(text.content)


def getdownurl(url):
    text = get_html(url).text
    re0 = r'<a onclick="upload\((.*?)\)"'
    fir_url = re.findall(re0, text)
    print(fir_url)
    if len(fir_url) == 0:
        return
    strurl = ''.join(e for e in fir_url[0])
    print(strurl)
    tpurl = re.split("','", strurl)
    endstp = []
    for ul in tpurl:
        elem = ul.strip('\'').strip('\'')
        endstp.append(elem)
    print(endstp, type(endstp[0]))
    head = 'http://www.wanfangdata.com.cn/search/downLoad.do?page_cnt='
    geturl = head + endstp[0] + "&language=" + endstp[2] + "&resourceType=" + endstp[6] + "&source=" + endstp[
        3] + "&resourceId=" + endstp[1] + "&resourceTitle=" + endstp[4] + "&isoa=" + endstp[5] + "&type=" + endstp[0]
    print('The download page url is: ' + geturl)
    # geturl = 'http://www.wanfangdata.com.cn/search/downLoad.do?page_cnt=51&language=chi&resourceType=degree&source=[WF, CNKI]&resourceId=D701708&resourceTitle=三毛的流浪人生与精神抒写&isoa=0&type=degree&first=null'
    re1 = r'<iframe style="display:none" id="downloadIframe" src="(.*?)">'
    text = get_html(geturl).text
    sucurl = re.findall(re1, text)
    print('资源下载地址：' + sucurl[0])
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
            try:
                re0 = r'<title>(.*?)</title>'
                text = get_html(url).text
                title = re.findall(re0, text)[0]
                print("下载：", title)
                geturl = getdownurl(url)
                get_pdf(geturl, title)
            except BaseException as e:
                print("下载失败：" + title)
                print(e)
                continue
            finally:
                print("all downloads is", num)


def post_json(url, param):
    res = requests.post(url, param)
    res.encoding = 'utf-8'
    text = res.text
    json_str = json.loads(text)
    return json_str


def main():
    with open(r'2018-11-16下午4-4-37@WanFangdata.txt', 'r') as f:
        paper_titles = f.readlines()
    for line in paper_titles:
        if len(line) > 5:
            title = line.lstrip('【篇名】').strip()
            downloadAllPdf(title)


if __name__ == '__main__':
    download_pdf(
        'http://caj.d.cnki.net//KDoc/docdown/pubdownload.aspx?dk=kdoc%3apdfdown%3a9e2c4793049e788f23f219e024765c84',
        'dd.pdf')
