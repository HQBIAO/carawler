# coding=utf-8
# date:下午3:46 
# author:chenjunbiao
import traceback
import sys
import logging
import requests
import threading
sys.path.append('/home/zengchuan/carawler/')
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from crawler.src.wanfang.orm import Mysql
from crawler.src.wiki.utilAgent import choose_ua

logging.basicConfig(filename="cnki.log", level=logging.DEBUG)


class DownCnkiThread(threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id

    def run(self):
        logging.debug("Starting " + self.name)
        main(self.thread_id)
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


#
# def resource_page(url):
#     html = get_html(url)
#     if not html:  # http请求失败
#         raise ConnectionError(url + '   请求失败')
#     bs = BeautifulSoup(html.text, 'html.parser')
#     a_tag = bs.select('a')[0]
#     link = a_tag['href']
#     return link
#
#
# def download_link(url):
#     return resource_page(url)


def main(t_id):
    mysql = Mysql.get_connection_instance(r'/Users/chenjunbiao/project/carawler/crawler/src/wanfang/db_config.txt')
    sql = "select id ,cnki,paper_title,title from new_C_D_reference_formatted where id%10="+str(t_id)+" AND get_from_cnki =0 AND  cnki LIKE '%cnki%'"
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


if __name__ == '__main__':
    # url1 = down_page('http://www.cnki.com.cn/Article/CJFDTotal-GWJX200802006.htm')
    # url2 = resource_page(url1)
    # url3 = download_link(url2)
    # if url1.contains('pdfdown'):
    #     type = 'pdf'
    # else:
    #     type = 'caj'
    # download_pdf(url3, "")
    for i in range(10):
        DownCnkiThread(i).start()
    # t0 = DownCnkiThread(0)
    # t1 = DownCnkiThread(1)
    # t2 = DownCnkiThread(2)
    # t3 = DownCnkiThread(3)
    # t4 = DownCnkiThread(4)
    # t5 = DownCnkiThread(5)
    # t6 = DownCnkiThread(6)
    # t7 = DownCnkiThread(7)
    # t8 = DownCnkiThread(8)
    # t9 = DownCnkiThread(9)
    # t0.start()
    # t1.start()
    # t2.start()
    # t3.start()
    # t4.start()
