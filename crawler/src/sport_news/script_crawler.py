# coding=utf-8
# date:下午7:33 
# author:chenjunbiao

import requests
from bs4 import BeautifulSoup
import json

url = "http://platform.sina.com.cn/sports_other/livecast\
_dateschedule?app_key=3633771828&date=2018-09-20&callback=getLivecastScheculeCallback"


def fetch_html():
    res = requests.get(url)
    res.encoding = 'utf-8'
    json_str = res.text.lstrip('getLivecastScheculeCallback(').rstrip(');')
    json_object = json.loads(json_str)
    print(json_object['result']['data'][0])


fetch_html()
