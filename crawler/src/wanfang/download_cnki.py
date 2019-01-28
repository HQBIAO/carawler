# coding=utf-8
# date:下午3:46 
# author:chenjunbiao
import traceback
import sys
import logging

import math
import requests
import threading

sys.path.append('/home/zengchuan/carawler/')
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from crawler.src.wanfang.orm import Mysql
from crawler.src.wiki.utilAgent import choose_ua
import pandas as pd

logging.basicConfig(filename="cnki.log", level=logging.DEBUG)


class DownCnkiThread(threading.Thread):
    def __init__(self, thread_id, ref_down_df=None):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.ref_down_df = ref_down_df

    # def run(self):
    #     logging.debug("Starting " + self.name)
    #     main(self.thread_id)
    #     logging.debug("Existing " + self.name)

    def run(self):
        logging.debug("Starting " + self.name)
        down_caj(self.ref_down_df, self.thread_id)
        logging.debug("Existing " + self.name)


class Cnki():
    def __init__(self, cookie="", ua=choose_ua()):
        self.cookie = cookie
        self.ua = ua

    def login(self, refer):
        """
        登录知网,重新设置cookie
        :param refer:
        :return:
        """
        header = {
            # 'Cookie': 'Ecp_ClientId=4181112101800794072; cnkiUserKey=80fd7e89-b248-38b3-fd19-00f0564e61bd; UM_distinctid=16705b7108be39-01f38d4e5a6a2e-594d2a16-1fa400-16705b7108c8b3',
            'Refer': refer,
            'User-Agent': choose_ua()
        }
        res = requests.get('http://login.cnki.net/', headers=header)
        self.cookie = res.request.headers['Cookie']
        self.ua = header['User-Agent']
        logging.debug('刷新cookie成功')
        logging.debug(self.cookie)

    def get_html(self, url):
        try:
            now = datetime.now()
            expire_time = get_c_m_expire(self.cookie)
            d = (expire_time - now).seconds
            if d < 60:  # cookie过期时间小于60秒，重新登录，刷新cookie
                self.login(url)
            header = {
                'User-Agent': self.ua,
                'Cookie': self.cookie}
            r = requests.get(url, headers=header, verify=False)
            r.encoding = r.apparent_encoding
            return r
        except Exception as e:
            print("has error:" + str(e))
            return None

    def down_page(self, url):
        html = self.get_html(url)
        if not html:  # http请求失败
            raise ConnectionError(url + '   请求失败')
        bs = BeautifulSoup(html.text, 'html.parser')
        button_caj = bs.select('#ty_caj')
        button_pdf = bs.select('#ty_pdf')
        button_down = button_caj[0] if button_caj else button_pdf[0]
        down_url = button_down.findChild('a')['href'].strip()
        return down_url

    def download_caj(self, url, save_path):
        html = self.get_html(url)
        with open(save_path, 'wb') as f:
            f.write(html.content)


def get_c_m_expire(cookie):
    if not cookie:
        return datetime.now()
    s = ''
    for c in cookie.split(';'):
        if 'c_m_expire' in c:
            s = c
            break

    return datetime.strptime(s.split('=')[1], "%Y-%m-%d %H:%M:%S")


def filter_essayBoxList(essayBoxList):
    box_list = []
    for essayBox in essayBoxList:
        db_title_text = essayBox.select('.dbTitle')[0].text
        if '中国学术期刊网络出版总库' in db_title_text or '国际期刊数据库' in db_title_text:
            box_list.append(essayBox)
    return box_list


def __get_ref_items(essayBoxList, CurDBCode='CJFQ', target_paper=""):
    db_title = 'not found'
    if CurDBCode == 'CJFQ':
        db_title = '中国学术期刊网络出版总库'
    if CurDBCode == 'CRLDENG':
        db_title = '外文题录数据库'
    if CurDBCode == 'SSJD':
        db_title = '国际期刊数据库'
    ref_items = []
    for essayBox in essayBoxList:
        if db_title in essayBox.select('.dbTitle')[0].text:
            ref_items = essayBox.find('ul').findAll('li')
            break
    ref_items_info = []

    for item in ref_items:
        text = item.text
        a_tag = item.find('a')
        ref_href = a_tag['href'] if a_tag else None
        ref_title = a_tag.text if a_tag else None
        ref_items_info.append(
            {'target_paper': target_paper,
             'ref_href': ref_href,
             'ref_title': ref_title,
             'text': text,
             'CurDBCode': CurDBCode
             })
    return ref_items_info


def html_bs(url):
    res = requests.get(url)
    res.encoding = 'utf-8'
    html = res.text
    return BeautifulSoup(html, 'html.parser')


def get_ref_list(detail_url, target_paper):
    """
    获取文章的参考文献列表（不需要登录）
    :param detail_url: 文章详情页url
    :return:
    """
    ref_list = []
    query_str = detail_url.split('?')[1]
    param_dict = {}
    for param in query_str.split('&'):
        param_pair = param.split('=')
        param_dict[param_pair[0]] = param_pair[1]

    url_pattern = 'http://kns.cnki.net/kcms/detail/frame/list.aspx?dbcode={}&filename={}&dbname={}\
    &RefType=1&page={}&CurDBCode={}'
    ref_url = url_pattern.format(
        param_dict['dbcode'], param_dict['filename'], param_dict['dbname'], '1', 'CJFQ')
    bs = html_bs(ref_url)

    essayBoxList = bs.select('.essayBox')
    essayBoxList = filter_essayBoxList(essayBoxList)

    china_journal = __get_ref_items(essayBoxList, CurDBCode='CJFQ', target_paper=target_paper)
    international_journal = __get_ref_items(essayBoxList, CurDBCode='SSJD', target_paper=target_paper)
    ref_list.extend(china_journal)
    ref_list.extend(international_journal)
    for essayBox in essayBoxList:
        # if '中国学术期刊网络出版总库' not in essayBox.select('.dbTitle')[0].text:
        #     continue
        # ref_items = essayBox.find('ul').findAll('li')
        # ref_items_info = __get_ref_items(ref_items)
        # print(ref_items_info)  # 分页导航栏
        page_bar = essayBox.select('.pageBar')
        if page_bar:
            CurDBCode = page_bar[0].find('span')['id']
            total_cnt = int(essayBox.find('span', {'name': 'pcount'}).text)
            page_cnt = int(math.ceil(total_cnt / 10))
            page_link_list = []
            for page_no in range(2, page_cnt + 1):
                page_link_list.append(url_pattern.format(
                    param_dict['dbcode'], param_dict['filename'], param_dict['dbname'], str(page_no), CurDBCode))
            for page_link in page_link_list:
                page_bs = html_bs(page_link)
                page_items = __get_ref_items(page_bs.select('.essayBox'), CurDBCode=CurDBCode,
                                             target_paper=target_paper)
                ref_list.extend(page_items)
    return ref_list


def get_down_url(detail_page_url, CurDBCode, domain='http://kns.cnki.net'):
    if not detail_page_url or isinstance(detail_page_url, float):
        return 'detail url not exist'
    bs = html_bs(domain + detail_page_url)
    if CurDBCode == 'CJFQ':
        down_btn = bs.select('#cajDown')
        down_btn = down_btn[0] if down_btn else None
        down_url = down_btn['href'] if down_btn else 'caj link not exist'
    else:
        down_btn = bs.select('#DownLoadParts')
        down_btn = down_btn[0] if down_btn else None
        down_url = down_btn.find('a')['href'] if down_btn else 'down link not exist'
    return down_url


def main(t_id):
    mysql = Mysql.get_connection_instance(r'db_config.txt')
    sql = "SELECT id ,cnki,paper_title,title FROM new_C_D_reference_formatted WHERE id%10=" + str(
        t_id) + " AND get_from_cnki =0 AND  cnki LIKE '%cnki%'"
    result = mysql.fetch_all(sql)
    cookie = 'Ecp_ClientId=4181112101800794072; cnkiUserKey\
    =80fd7e89-b248-38b3-fd19-00f0564e61bd; UM_distinctid=16705b7108be39-01f38d4e5a6a2e-594d2a16-1fa400-16705b7108c8b3'
    cnki = Cnki()
    for row in result:
        id = row[0]
        cnki_url = row[1]
        paper_title = row[2]
        title = row[3]
        try:
            url1 = cnki.down_page(cnki_url)
            suffix = '.pdf' if 'pdfdown' in url1 else '.caj'
            save_path = Path.home().joinpath('cnki', paper_title)
            if not save_path.exists():
                save_path.mkdir(parents=True)
            save_path = save_path.joinpath(title + suffix)
            cnki.download_caj(url1, str(save_path))
            update_sql = "update new_C_D_reference_formatted set get_from_cnki = 1 where id =%d" % (id)
            mysql.update(update_sql)
            logging.debug(paper_title + "-------" + title + ":下载成功")
        except Exception as e:
            logging.debug(paper_title + "-------" + title + ":下载是失败")
            t, v, tb = sys.exc_info()
            logging.debug(traceback.format_exception(t, v, tb))


def down_caj(ref_down_df, t_id):
    a = ref_down_df[ref_down_df.index.values % 10 == t_id]
    a = a[a['CurDBCode'] == 'CJFQ']
    file_download_status_df = pd.DataFrame(columns=['uuid', 'title', 'success'])
    cnki = Cnki()
    for index, row in a.iterrows():
        down_link = row['down_link']
        # 下载链接不存在
        if down_link.startswith('http'):
            file_download_status_df = file_download_status_df.append(
                {'uuid': row['uuid'], 'title': row['ref_title'], 'success': 'download link not found'},
                ignore_index=True)
            continue
        save_path = Path.home().joinpath('finance', row['target_paper'])
        if not save_path.exists():
            save_path.mkdir(parents=True)
        save_path = save_path.joinpath(row['ref_title'] + "&&" + row['uuid'] + '.caj')
        try:
            cnki.download_caj(down_link, str(save_path))
            file_download_status_df = file_download_status_df.append(
                {'uuid': row['uuid'], 'title': row['ref_title'], 'success': '1'}, ignore_index=True)
            logging.debug(row['target_paper'] + "-------" + row['ref_title'] + ":下载成功")
        except Exception as e:
            file_download_status_df = file_download_status_df.append(
                {'uuid': row['uuid'], 'title': row['ref_title'], 'success': '0'}, ignore_index=True)
            logging.debug(row['target_paper'] + "-------" + row['ref_title'] + ":下载失败")
            logging.debug(e)
    result_path = Path.cwd().parent.joinpath('data')
    if not result_path.exists():
        result_path.mkdir(parents=True)
    file_download_status_df.to_csv(str(result_path.joinpath('file_download_status_' + str(t_id) + '.csv')), index=False)


if __name__ == '__main__':
    for i in range(10):
        DownCnkiThread(i, pd.read_csv('down_df.csv')).start()
