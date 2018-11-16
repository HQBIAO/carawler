# coding=utf-8
import requests
import time
from bs4 import BeautifulSoup
import re
import urllib.request as ulbr
import pandas as pd
from src.wiki.utilAgent import *


class FigureRelation(object):
    def __init__(self, previous_person, current_person):
        self.previous_person = previous_person
        self.current_person = current_person


class WikiPerson(object):
    def __init__(self, base_key, deep, relation_path, context_path):
        self.__person_set = set()
        self.__baseUrl = 'https://zh.wikipedia.org'
        self.__baseKey = base_key
        self.figure_relation_list = []


def filter_person(link, current_person):
    title_attr = link.attrs['title']
    title_len = len(title_attr)
    if 'href' in link.attrs and title_len in [2, 3]:
        print(link)
        if title_attr[-1] in ('省', '市', '县', '区', '镇', '乡', '村') or title_attr in total_people_set:
            return None
        if [title_attr, current_person] in result:
            return None
        if not is_name(title_attr):
            return None
        return title_attr


def get_relative_people(url, current_person):
    sleep_time = random.randint(10, 30)
    time.sleep(sleep_time)
    headers['User-Agent'] = choose_ua()
    try:
        response = requests.get(url)
        # response = requests.get(url, headers=headers)
    except:
        print('访问失败: ', response.status_code)
        # time.sleep(60)
        return []
    response.encoding = 'utf-8'
    text = response.text
    html = BeautifulSoup(text, "lxml")
    content = html.find("div", {"id": "bodyContent"})
    person_list = []
    for link in content.findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
        person = filter_person(link, current_person)
        if person:
            person_list.append(person)
    return list(set(person_list))


def construct_relation(person_name, relative_person_list):
    return [[person_name, relative_person_name] for relative_person_name in relative_person_list]


def is_name(key_word):
    if len(key_word) == 2:
        return key_word[:1] in first_name
    if len(key_word) == 3:
        return key_word[:1] in first_name or key_word[0:2] in first_name
    return False


result = []


def get_content(key_word):
    base_url = 'https://zh.wikipedia.org/wiki/'
    res = requests.get(base_url + ulbr.pathname2url(key_word))
    res.encoding = 'utf-8'
    the_html = BeautifulSoup(res.text, "lxml")
    # print(__get_content(the_html))
    content = the_html.find("div", {"id": "bodyContent"})
    contents = []
    for ele in content.findAll({"h1", "h2", "h3", "h4", "h5", "h6", "p"}):
        # file.write(str(ele)[2] + " " + ele.get_text() + "\n")
        contents.append(str(ele)[2] + " " + ele.get_text())
    return contents


if __name__ == '__main__':
    first_name = '王,李,张,刘,陈,杨,黄,赵,吴,周,徐,孙,马,朱,胡,郭,何,高,林,罗,郑,梁,谢,宋,唐,' \
                 '许,韩,冯,邓,曹,彭,曾,肖,田,董,袁,潘,于,蒋,蔡,余,杜,叶,程,苏,魏,吕,丁' \
                 ',任,沈,姚,卢,姜,崔,钟,谭,陆,汪,范,金,石,廖,贾,夏,韦,傅,方,白,邹,孟,熊,秦' \
                 ',邱,江,尹,薛,闫,段,雷,侯,龙,史,陶,黎,贺,顾,毛,郝,龚,邵,万,钱,严,乔,武,戴,莫' \
                 ',孔,向,汤,艾,安,包,保,鲍,查,柴,敖,巴,柏,班,贝,毕,卞,卜,步,苍,岑,昌,常,晁,巢,' \
                 '车,成,池,仇,储,楚,褚,笪,单,党,狄,刁,东,都,窦,法,樊,房,费,丰,封,酆,凤,伏,符,福,' \
                 '付,富,盖,甘,干,郜,戈,葛,耿,公,宫,巩,贡,勾,古,谷,关,管,光,广,归,桂,国,哈,海,杭,' \
                 '和,弘,红,洪,后,花,华,怀,桓,宦,惠,霍,姬,嵇,吉,籍,计,纪,季,冀,简,焦,解,靳,经,荆,' \
                 '井,景,居,鞠,阚,康,柯,寇,蒯,匡,赖,兰,蓝,郎,劳,乐,冷,厉,利,郦,栗,连,廉,蔺,凌,柳,' \
                 '娄,鲁,路,栾,骆,麻,满,茅,梅,蒙,米,苗,明,缪,墨,牟,慕,穆,那,能,倪,年,聂,宁,牛,钮,' \
                 '庞,裴,皮,平,蒲,濮,朴,浦,戚 ,齐,祁,千,强,丘,秋,裘,屈,瞿,曲,权,全,阙,冉,饶,戎,荣,' \
                 '容,茹,汝,阮,芮,桑,沙,山,商,尚,佘,申,慎,盛,师,施,时,寿,殳,舒,束,帅,双,水,司,松,索' \
                 ',谈,滕,佟,童,涂,屠,危,卫,温,文,闻,翁,沃,乌,邬,巫,伍,郗,奚,习,席,相,项,萧,辛,邢,' \
                 '幸,胥,宣,荀,鄢,言,阎,晏,燕,羊,阳,仰,伊,易,阴,殷,印,应,雍,尤,游,鱼,俞,虞,禹,庾,郁,' \
                 '喻,元,岳,云,臧,翟,詹,展,湛,章,甄,支,仲,诸,竺,祝,庄,卓,宗,祖,左,,百里,淳于,澹台,第五' \
                 ',东方,东郭,东门,段干,公良,公孙,公西,公羊,公冶,谷粱,赫连,呼延,皇甫,夹谷,乐正,梁丘,令狐' \
                 ',闾丘,慕容,南宫,南门,欧阳,濮阳,漆雕,' \
                 '亓官,壤驷,上官,申屠,司空,司寇,司马,司徒,太叔,拓拔,微生,尉迟,巫马,西门,夏侯,鲜' \
                 '于,轩辕,羊舌,宇文,宰父,长孙,钟离,仲孙,诸葛,颛孙,子车,宗政,左丘,'
    total_people_set = set(['陈独秀'])
    base_url = 'https://zh.wikipedia.org/wiki/'
    person_list_to_extend = ['陈独秀']  # 待扩展的人物列表
    res = requests.get(base_url + ulbr.pathname2url('陈独秀'))
    res.encoding = 'utf-8'
    the_html = BeautifulSoup(res.text, "lxml")
    print(get_content(the_html))
    # while True:
    #     person = person_list_to_extend.pop(0)
    #     url = base_url + ulbr.pathname2url(person)
    #     relative_people = get_relative_people(url, person)  # 找出与当前人物的相关的人物列表
    #     if relative_people:
    #         result.extend(construct_relation(person, relative_people))  # 构造当前人物与相关人物的联系
    #         total_people_set = total_people_set.union(relative_people)
    #         person_list_to_extend.extend(relative_people)
    #     if len(total_people_set) > 10000:
    #         pd.DataFrame(result).to_csv("figure_relation.csv", index=None)
    #         break
