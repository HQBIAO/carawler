import requests
from bs4 import BeautifulSoup

url = 'http://news.sina.com.cn/s/2018-03-13/doc-ifysfemy5598870.shtml'  # 新闻的地址


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


# print(get_news_info('http://news.sina.com.cn/s/2018-03-13/doc-ifysfemy5598870.shtml'))
# print(get_news_info('http://news.sina.com.cn/s/wh/2018-03-13/doc-ifyscsmv1291827.shtml'))
for i in range(100000):
    print(requests.get(url))