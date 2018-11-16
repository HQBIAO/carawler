# coding=utf-8
import random

import pymysql
import requests
import urllib.request as ulbr

import time
from bs4 import BeautifulSoup


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
    db = pymysql.connect("112.74.189.216", "root", "Qwe@1234", "wiki", charset='utf8')
    cursor = db.cursor()
    select_sql = "SELECT * FROM figure_name  WHERE has_text = '%d' limit 1" % (0)
    while True:
        sleep_time = random.randint(1, 15)
        time.sleep(sleep_time)
        cursor.execute(select_sql)
        results = cursor.fetchone()
        if not results:
            break
        name = results[0]
        has_exception = False
        try:
            content = get_content(name)
            with open('../data/' + name + '.txt', 'w') as f:
                for item in content:
                    f.write(item + '\n')
            print(results)
        except:
            has_exception = True
            sleep_time = random.randint(300, 500)
            time.sleep(sleep_time)
        try:
            if not has_exception:
                update_sql = "UPDATE figure_name SET has_text = 1 WHERE name = '%s'" % (name)
                cursor.execute(update_sql)
                db.commit()
        except:
            db.rollback()
    cursor.close()
