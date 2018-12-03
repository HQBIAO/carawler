# coding=utf-8
# date:下午8:48 
# author:chenjunbiao
import random
import re

import time

import os
import sys
from bs4 import BeautifulSoup
from pandas import DataFrame

sys.path.append('/home/zengchuan/carawler/')
from crawler.src.wanfang.readpdf import Mysql
from papers import get_html, get_pdf, post_json, download_pdf
import pandas as pd
import json
import math


def __source_url__(down_page_url):
    """
    获取资源的下载地址
    :param down_page_url:下载页面的地址
    :return:
    """
    print('The download page url is: ' + down_page_url)
    re1 = r'<iframe style="display:none" id="downloadIframe" src="(.*?)">'
    text = get_html(down_page_url).text
    source_url = re.findall(re1, text)
    return source_url[0]


def extract_download_url(text):
    bs = BeautifulSoup(text, 'html.parser')
    a_tag_down = bs.select('.result_opera_down')
    if len(a_tag_down) < 1 and 'onclick' not in a_tag_down[0]:
        return None, None
    print(a_tag_down[0]['onclick'])
    tp_list = [tag['onclick'].lstrip('downLoad(').rstrip(')').split("','") for tag in a_tag_down]
    print(tp_list)
    down_urls = []
    titles = []
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
        source_url = __source_url__(geturl)
        print('资源下载地址：' + source_url)
        down_urls.append(source_url)
    return down_urls, titles


def get_degree_papers(page_start, page_end):
    base_url = 'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=degree&pageSize=20&page={}&searchWord=学位授予单位:暨南大学&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&facetField=$subject_classcode_level:∷/H*$degree_level:硕士&facetName=硕士:$degree_level*语言、文字:$subject_classcode_level&firstAuthor=false&rangeParame=&navSearchType=degree'
    for index in range(page_start, page_end + 1):
        url = str.format(base_url, str(index))
        html = get_html(url).text
        down_urls, titles = extract_download_url(html)
        if not down_urls:
            continue
        for i in range(len(down_urls)):
            sleep_time = random.randint(1, 10)
            time.sleep(sleep_time)
            print("开始下载第" + str(index) + "页的：" + titles[i] + " ----------------------------------")
            get_pdf(down_urls[i], titles[i], index)


def title_id_pair(page_start, page_end):
    base_url = 'http://www.wanfangdata.com.cn/search/searchList.do?beetlansyId=aysnsearch&searchType=degree&pageSize=20&page={}&searchWord=学位授予单位:暨南大学&order=correlation&showType=detail&isCheck=check&isHit=&isHitUnit=&facetField=$subject_classcode_level:∷/H*$degree_level:硕士&facetName=硕士:$degree_level*语言、文字:$subject_classcode_level&firstAuthor=false&rangeParame=&navSearchType=degree'
    ids = []
    titles = []
    for index in range(page_start, page_end + 1):
        url = str.format(base_url, str(index))
        html = get_html(url).text
        bs = BeautifulSoup(html, 'html.parser')
        title_tags = bs.select('.ResultCont .title')
        for title in title_tags:
            try:
                a_tags = title.findChildren('a')
                if len(a_tags) < 3:
                    paper_title = a_tags[0].text
                    paper_id = a_tags[1].findChild('i')['onclick'].lstrip('showBox(').rstrip(')').split(',')[1].strip(
                        "'")
                else:
                    paper_id = a_tags[0]['onclick'].lstrip("chap('").rstrip("');")
                    paper_title = a_tags[1].text
            except BaseException as e:
                paper_id = None
                paper_title = None
                print title
                print e

            ids.append(paper_id)
            titles.append(paper_title)
    return ids, titles


def save_title_id_pair(page_start, page_end, save_path):
    ids, titles = title_id_pair(page_start, page_end)
    df_title_id = DataFrame({'titles': titles, 'ids': ids})
    df_title_id.to_csv(save_path, encoding='utf-8')


def get_reference_in_wanfang(paper_id):
    """
    获取一篇文章在万方数据库的参考文献
    :param paper_id:文章id
    :return:文章id为paper_id的参考文献列表
    """
    number = 1
    url = 'http://www.wanfangdata.com.cn/graphical/turnpage.do'
    param = {'type': 'reference', 'id': paper_id, 'number': number}
    fetch_count = 0
    reference_list = []
    while True:
        result = post_json(url, param)
        sub_reference_list = result[0]
        fetch_count += len(sub_reference_list)
        reference_list.extend(sub_reference_list)
        reference_count = int(result[1])
        number += 1
        param['number'] = number
        if fetch_count == reference_count:
            break
    return reference_list


def get_batch_reference(title_id_pair):
    """
    批量获取参考文献
    :param title_id_pair:
    :return:
    """
    df_references = None
    is_null = True
    for index, row in title_id_pair.iterrows():
        paper_title = row['paper_title']
        paper_id = row['paper_id']
        try:
            reference = get_reference_in_wanfang(paper_id)
        except BaseException as e:
            print e
            print row, '获取失败'
        df_reference = DataFrame(reference)
        df_reference['paper_title'] = paper_title
        df_reference['paper_id'] = paper_id
        if is_null:
            df_references = df_reference
            is_null = False
        else:
            df_references = pd.concat([df_references, df_reference])
    return df_references


def ref_download_page(type, id):
    """
    参考文献下载页面的地址
    :param type: 文献类型
    :param id: 文献id
    :return:
    """
    url = "http://www.wanfangdata.com.cn/asynRetrieval/docPaper.do"
    param = {"_type": type,
             "id": id,
             "number": 1,
             "first": 'undefined'}
    result = None
    try:
        result = post_json(url, param)
    except BaseException as e:
        print url + "   请求失败"
        print e
    result = json.loads(result)
    ll = None
    try:
        ll = "http://www.wanfangdata.com.cn/search/downLoad.do?language=" + result[
            'language'] + "&resourceType=" + type + "&source=" + result['source_db'][0] + "&resourceId=" + result[
                 'article_id'] + "&resourceTitle=" + result['title'] + ""
    except BaseException as e:
        print "下载页地址拼接失败"
        print e
    return ll


def down_ref(ref_down_url, save_path):
    source_url = __source_url__(ref_down_url)
    # todo
    download_pdf(source_url, save_path)


def batch_down_ref():
    with open(r'db_config.txt', 'r') as f:
        line = f.readline()
        db_config = line.split(',')
    mysql = Mysql(db_config[0], db_config[1], db_config[2], db_config[3])
    mysql.connect()
    select_sql = "SELECT ArticaleId,Title,paper_title,paper_id,Degree,Periodical,id,Symbol FROM reference_title  \
        WHERE HasFulltext = '%s' AND download = %d AND try_times =0 limit 1" % (True, 0)
    result = mysql.fetch_one(select_sql)
    while result:
        id = result[6]
        ArticaleId = result[0]
        ArticaleId = ArticaleId[0:ArticaleId.index('^')] if '^' in ArticaleId else ArticaleId
        Title = result[1]
        paper_title = result[2]
        paper_id = result[3]
        symbol = result[7]
        old_Title = Title
        if '%' in Title:
            Title = Title.split('%')[0]
        dir_path = 'data/' + paper_title
        dir_path = os.path.abspath(dir_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        save_path = dir_path + '/' + Title + '.pdf'
        # 文件已存在，跳过下载
        if os.path.exists(save_path):
            update_down_sql = "update reference_title set download = 1 WHERE id='%d'" % (id)
            mysql.update(update_down_sql)
            print save_path + u" ======已存在"
            continue
        ref_type = ""
        if result[4]:
            ref_type = 'degree'
        if result[5]:
            ref_type = 'perio'
        if symbol == 'Conference':
            ref_type = 'conference'
        update_sql = "UPDATE reference_title SET download = 1 WHERE id = '%d' AND download = 0" % (id)
        download_page_url = ref_download_page(ref_type, ArticaleId)
        try:
            down_ref(download_page_url, save_path)
            mysql.update(update_sql)
        except BaseException as e:
            print Title + u"--------下载失败"
            update_try_times = "UPDATE reference_title SET try_times = try_times+1  WHERE id = '%d' AND download = 0" % (
                id)
            mysql.update(update_try_times)
            print e
        result = mysql.fetch_one(select_sql)


if __name__ == '__main__':
    # get_degree_papers(1, 10)
    # get_degree_papers(5, 10)
    batch_down_ref()
