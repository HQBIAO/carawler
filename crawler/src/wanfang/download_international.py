# coding=utf-8
# date:2019/2/1 下午7:45 
# author:chenjunbiao
import platform
from pathlib import Path

import pandas as pd
import re
from bs4 import BeautifulSoup
from selenium import webdriver


def get_introduction(bs):
    body_div = bs.find('div', {'id': 'body'})
    if not body_div:
        return 'body do not exist'
    sections = body_div.findAll('section')
    intro_sec = None
    for section in sections:
        h2 = section.find(re.compile('^h[1-6]$'))
        if not h2:
            continue
        little_title = h2.text.lower()
        if 'introduction' in little_title:
            intro_sec = section
            continue

    introduction_text = ""
    if not intro_sec:
        return 'introduction section do not exist'
    for p in intro_sec.findAll('p'):
        introduction_text += p.text
    return introduction_text


def get_conclusion(bs):
    body_div = bs.find('div', {'id': 'body'})
    if not body_div:
        return 'body do not exist'
    sections = body_div.findAll('section')
    conclu_sec = None
    for section in sections:
        h2 = section.find(re.compile('^h[1-6]$'))
        if not h2:
            continue
        little_title = h2.text.lower()
        if 'conclusion' in little_title:
            conclu_sec = section
    conclusion_text = ""
    if not conclu_sec:
        return 'conclusion section do not exist'
    for p in conclu_sec.findAll('p'):
        conclusion_text += p.text
    return conclusion_text


def get_abstract(bs):
    abstract = bs.select('#abstracts')
    if abstract:
        return abstract[0].text
    else:
        return ""


def get_en_paper(url, abstract_func, introduction_func, conclusion_func):
    if platform.system() == 'Windows':
        driver = webdriver.Chrome(r'C:\Users\lvzen\AppData\Local\Google\Chrome\Application\chromedriver.exe')
    else:
        driver = webdriver.Chrome()
    driver.get(url)
    bs = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()
    abstract_text = abstract_func(bs)
    introduction_text = introduction_func(bs)
    conclusion_text = conclusion_func(bs)
    return {'abstract_text': abstract_text, 'introduction_text': introduction_text, 'conclusion_text': conclusion_text}


if __name__ == '__main__':
    down_df = pd.read_csv('down_df.csv')
    down_en_df = down_df[down_df['res'].notnull()]
    for index, row in down_en_df.iterrows():
        save_path = Path.home().joinpath('sciencedirect', row['target_paper'], row['ref_title'])
        if not save_path.exists():
            save_path.mkdir(parents=True)

        if 'sciencedirect' in row['res']:
            content_dict = get_en_paper(row['res'], get_abstract, get_introduction, get_conclusion)
            for k, v in content_dict.items():
                if len(v) < 30:
                    file_name = row['ref_title'] + '&&' + row['uuid'] + '&&' + k + '&&empty.txt'
                else:
                    file_name = row['ref_title'] + '&&' + row['uuid'] + '&&' + k + '&&exist.txt'
                with save_path.joinpath(file_name).open('w') as f:
                    f.write(v)
            print(content_dict)
