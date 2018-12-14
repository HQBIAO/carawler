# coding=utf-8
# date:下午8:49 
# author:chenjunbiao
import urllib

import re
from bs4 import BeautifulSoup

from crawler.src.wanfang.papers import get_html

from crawler.src.wanfang.orm import Mysql
import pandas as pd
from crawler.src import common_utlis


def get_accurate_match(title):
    html = get_html('http://xueshu.baidu.com/s?wd=' + title + '&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&sc_hit=1')
    if not html:  # http请求失败
        raise ConnectionError('http 请求失败')
    bs = BeautifulSoup(html.text, 'html.parser')

    try:
        result_el = bs.select('.result')[0]
        title_el = result_el.findChild('h3')
        title_txt = common_utlis.filter_chi_char(title_el.text)
        em_count = len(title_el.findAll('em'))
        if em_count <= 1 or title_txt == common_utlis.filter_chi_char(title):
            detail_url = title_el.findChild('a')['href']
            source_el = result_el.select('.c_allversion')
            source_str = source_el[0].text.strip().replace('\n', '').replace(' ', '')
            return {'detail_url': detail_url, 'source_str': source_str}
        else:
            return None
    except:
        raise FileNotFoundError('')


def show_page(url):
    """
    这里用正则匹配会有bug
    例如：wd=paperuri:(a7738615346efde5e7ae1922a5ee4b71)&filter=sc_long_sign&sc_ks_para=q=认知语言学研究综述(一)&sc_us=255587085528750776&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8
    会得到错误的结果：http://xueshu.baidu.com/usercenter/paper/show?paperid=a7738615346efde5e7ae1922a5ee4b71)&filter=sc_long_sign&sc_ks_para=q=认知语言学研究综述(一&site=xueshu_se
    :param url:
    :return:
    """

    def f(s):
        if not isinstance(s, float) and s != 'not found':
            decode_s = urllib.parse.unquote(s)
            paper_id = re.findall('\(.*\)', decode_s)[0].lstrip('(').rstrip(')')
            return 'http://xueshu.baidu.com/usercenter/paper/show?paperid={}&site=xueshu_se'.format(paper_id)
        else:
            return ''

    C_D_reference_formatted = pd.read_csv('paper_C_D_reference_formatted.csv')
    C_D_reference_formatted['show_page_url'] = C_D_reference_formatted.apply(lambda x: f(x['detail_url']), axis=1)


def batch_show_page_url():
    mysql = Mysql.get_connection_instance(r'/Users/chenjunbiao/project/carawler/crawler/src/wanfang/db_config.txt')
    sql = "select id ,detail_url from new_C_D_reference_formatted where detail_url is not null and detail_url != 'not found' and show_page_url is null "
    results = mysql.fetch_all(sql)
    for row in results:
        id = row[0]
        detail_url = row[1]
        decode_s = urllib.parse.unquote(detail_url).split('&')[0]
        paper_id = re.findall('\(.*\)', decode_s)[0].lstrip('(').rstrip(')')
        show_page_url = 'http://xueshu.baidu.com/usercenter/paper/show?paperid={}&site=xueshu_se'.format(paper_id)
        update_down_sql = "update new_C_D_reference_formatted set show_page_url='%s' WHERE id=%d" % (
            show_page_url, id)
        mysql.update(update_down_sql)


def get_cnki_page(url):
    html = get_html(url)
    if not html:  # http请求失败
        raise ConnectionError('http 请求失败')
    bs = BeautifulSoup(html.text, 'html.parser')
    try:
        all_source = bs.select('.allversion_content')[0]
        source_span_tags = all_source.select('.dl_item_span')
        chki_url = ""
        for tag in source_span_tags:
            source_name = tag.text.strip()
            a_tag = tag.findChild('a')
            if a_tag:
                chki_url = a_tag['data-url']
            if '知网' in source_name:
                break
        return chki_url
    except:
        raise FileNotFoundError('')


def batch_cnki_page():
    with open(r'db_config.txt', 'r') as f:
        line = f.readline()
        db_config = line.split(',')
    mysql = Mysql(db_config[0], db_config[1], db_config[2], db_config[3])
    mysql.connect()

    # def correct_show_page_url(s):
    #     return s.split(')&')[0] + '&site=xueshu_se'

    for i in range(1, 2020):
        select_sql = "SELECT id, show_page_url FROM new_C_D_reference_formatted  \
            WHERE show_page_url IS NOT NULL AND cnki is NULL AND id = %d limit 1" % (i)
        result = mysql.fetch_one(select_sql)
        if not result:
            continue
        uid = result[0]
        show_page_url = result[1]
        # show_page_url = correct_show_page_url(result[1])
        try:
            cnki_url = get_cnki_page(show_page_url)
            if cnki_url:
                update_down_sql = "update new_C_D_reference_formatted set cnki='%s' WHERE id=%d" % (cnki_url, uid)
            else:
                update_down_sql = "update new_C_D_reference_formatted set cnki='%s' WHERE id=%d" % ('-', uid)
            mysql.update(update_down_sql)
        except ConnectionError as ce:
            print(ce)
        except FileNotFoundError as fe:
            print(fe)


def batch_accurate_match():
    with open(r'db_config.txt', 'r') as f:
        line = f.readline()
        db_config = line.split(',')
    mysql = Mysql(db_config[0], db_config[1], db_config[2], db_config[3])
    mysql.connect()

    for i in range(2, 2020):
        select_sql = "SELECT id, title FROM new_C_D_reference_formatted  \
            WHERE source IS NULL AND id = %d limit 1" % (i)
        result = mysql.fetch_one(select_sql)
        if not result:
            continue
        uid = result[0]
        title = result[1]
        try:
            source = get_accurate_match(title)
            if source:
                detail_url = source['detail_url']
                source_str = source['source_str']
                update_down_sql = "update new_C_D_reference_formatted set fetch_times = 1,detail_url='%s',source='%s' WHERE id=%d" % (
                    detail_url, source_str, uid)
            else:
                update_down_sql = "update new_C_D_reference_formatted set fetch_times = 1,detail_url='%s' WHERE id=%d" % (
                    'not found', uid)
            mysql.update(update_down_sql)
        except ConnectionError as ce:
            print(ce)
        except FileNotFoundError as fe:
            print(fe)


if __name__ == '__main__':
    batch_cnki_page()
