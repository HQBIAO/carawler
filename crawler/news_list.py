import json

import time
import xlwt
from bs4 import BeautifulSoup

import requests


def get_news_list_url(page):
    news_url_list = []
    news_url = 'http://api.roll.news.sina.com.cn/zt_list?' \
               'channel=news&cat_1=shxw&cat_2==zqsk||=qwys' \
               '||=shwx||=fz-shyf&level==1||=2&show_ext=1&' \
               'show_all=1&show_num=22&tag=1&format=json&' \
               'page={}&callback=newsloadercallback&_=1521009222105'
    news_url = news_url.format(page)
    res = requests.get(news_url)
    # res.encoding = 'utf-8'
    dict_result = json.loads(res.text.lstrip('  newsloadercallback(').rstrip(');'))
    news_list_data = dict_result['result']['data']
    for news_item in news_list_data:
        news_url_list.append(news_item['url'])
    return news_url_list


def get_news_info(news_url):
    result = {}
    response = requests.get(news_url)  # 使用get方法获取地址对应的资源
    response.encoding = 'utf-8'  # 设置'utf-8'编码
    soup = BeautifulSoup(response.text, 'html.parser')  # 使用BeautifulSoup读取内容，并且设定解析器为html.parser
    title_tag = soup.select('h1')[1]  # 选择标题的标签
    content_tags = soup.select('p')  # 选择正文的标签
    source_tag = soup.select('.source')[0]  # 选择文章来源的标签
    time_tag = soup.select('.date')[0]  # 选择发表时间的标签
    contents_text = ""
    for content_tag in content_tags:
        '''循环取得每个段落的文本，并拼接起来'''
        contents_text += content_tag.text
    result['title'] = title_tag.text  # 将标题文本存储在result字典
    result['content'] = contents_text  # 将文章内容文本存储在result字典
    result['source'] = source_tag.text  # 将文章来源文本存储在result字典
    result['time'] = time_tag.text  # 将文章发表时间文本存储在result字典
    return result


news_info_list = []
for page in range(1, 2):
    news_list_url = get_news_list_url(page)
    for news_url in news_list_url:
        news_info_list.append(get_news_info(news_url))
        time.sleep(3)

book = xlwt.Workbook(encoding='utf-8')
sheet = book.add_sheet("my_sheet")
sheet.write(0, 0, '标题')
sheet.write(0, 1, '来源')
sheet.write(0, 2, '时间')

for index, news_info in enumerate(news_info_list):
    sheet.write(index+1,0,news_info['title'])
    sheet.write(index+1,1,news_info['source'])
    sheet.write(index+1,2,news_info['time'])

book.save('news_info.xls')

