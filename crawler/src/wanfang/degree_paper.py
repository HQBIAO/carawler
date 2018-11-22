# coding=utf-8
# date:下午8:48 
# author:chenjunbiao
import random
import re

import time
from bs4 import BeautifulSoup

from crawler.src.wanfang.papers import get_html, get_pdf


def extract_download_url(text):
    bs = BeautifulSoup(text, 'html.parser')
    a_tag_down = bs.select('.result_opera_down')
    print(a_tag_down[0]['onclick'])
    tp_list = [tag['onclick'].lstrip('downLoad(').rstrip(')').split("','") for tag in a_tag_down]
    print(tp_list)
    down_urls = []
    titles=[]
    for tp in tp_list:
        endstp = [el.strip("'") for el in tp]
        head = 'http://www.wanfangdata.com.cn/search/downLoad.do?page_cnt='
        geturl = head + endstp[0] + "&language=" + endstp[1] + "&resourceType=" + endstp[2] + "&source=" + endstp[
            3] + "&resourceId=" + endstp[4] + "&resourceTitle=" + endstp[5] + "&isoa=" + endstp[6] + "&type=" + endstp[
                     2]
        titles.append(endstp[5])
        # geturl = 'http://www.wanfangdata.com.cn/search/downLoad.do?page_cnt=51\
        # &language=chi&resourceType=degree&source=[WF, CNKI]&resourceId=D701708&resourceTitle=三毛的流浪人生与精神抒写\
        # &isoa=0&type=degree&first=null'
        print('The download page url is: ' + geturl)
        re1 = r'<iframe style="display:none" id="downloadIframe" src="(.*?)">'
        text = get_html(geturl).text
        source_url = re.findall(re1, text)
        print('资源下载地址：' + source_url[0])
        down_urls.append(source_url[0])
    return down_urls,titles


def get_degree_papers(page_start, page_end):
    base_url = 'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=degree&pageSize=20&page={}&searchWord=学位授予单位:暨南大学&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&facetField=$subject_classcode_level:∷/H*$degree_level:硕士&facetName=硕士:$degree_level*语言、文字:$subject_classcode_level&firstAuthor=false&rangeParame=&navSearchType=degree'
    for index in range(page_start, page_end + 1):
        url = str.format(base_url, str(index))
        html = get_html(url).text
        down_urls,titles = extract_download_url(html)
        for i in range(len(down_urls)):
            sleep_time = random.randint(1,10)
            time.sleep(sleep_time)
            print("开始下载："+titles[i]+" ----------------------------------")
            get_pdf(down_urls[i],titles[i])

if __name__=='__main__':
    get_degree_papers(1, 10)
