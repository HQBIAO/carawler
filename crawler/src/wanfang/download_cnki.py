# coding=utf-8
# date:下午3:46 
# author:chenjunbiao
from bs4 import BeautifulSoup

from crawler.src.wanfang.orm import Mysql
from crawler.src.wanfang.papers import get_html, download_pdf
from pathlib import Path


def down_page(url):
    html = get_html(url)
    if not html:  # http请求失败
        raise ConnectionError(url + '   请求失败')
    bs = BeautifulSoup(html.text, 'html.parser')
    button_caj = bs.select('#ty_caj')
    button_pdf = bs.select('#ty_pdf')
    button_down = button_caj[0] if button_caj else button_pdf[0]
    down_url = button_down.findChild('a')['href'].strip()
    return down_url


def resource_page(url):
    html = get_html(url)
    if not html:  # http请求失败
        raise ConnectionError(url + '   请求失败')
    bs = BeautifulSoup(html.text, 'html.parser')
    a_tag = bs.select('a')[0]
    link = a_tag['href']
    return link


def download_link(url):
    return resource_page(url)


def main():
    mysql = Mysql.get_connection_instance(r'/Users/chenjunbiao/project/carawler/crawler/src/wanfang/db_config.txt')
    sql = "select id ,cnki,paper_title,title from new_C_D_reference_formatted where cnki LIKE '%cnki%' AND get_from_cnki =0"
    result = mysql.fetch_all(sql)
    for row in result:
        id = row[0]
        cnki = row[1]
        paper_title = row[2]
        title = row[3]

        url1 = down_page(cnki)
        # url2 = resource_page(url1)
        # url3 = download_link(url2)
        suffix = '.pdf' if 'pdfdown' in url1 else '.caj'
        save_path = Path.home().joinpath('cnki', paper_title)
        if not save_path.exists():
            save_path.mkdir(parents=True)
        save_path = save_path.joinpath(title + suffix)
        download_pdf(url1, str(save_path))
        update_sql = "update new_C_D_reference_formatted set get_from_cnki = 1 where id =%d" % (id)
        mysql.update(update_sql)


if __name__ == '__main__':
    # url1 = down_page('http://www.cnki.com.cn/Article/CJFDTotal-GWJX200802006.htm')
    # url2 = resource_page(url1)
    # url3 = download_link(url2)
    # if url1.contains('pdfdown'):
    #     type = 'pdf'
    # else:
    #     type = 'caj'
    # download_pdf(url3, "")
    main()
