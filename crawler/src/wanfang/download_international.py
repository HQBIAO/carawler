# coding=utf-8
# date:2019/2/1 下午7:45 
# author:chenjunbiao

import pandas as pd
import requests

from crawler.src.wanfang.download_cnki import html_bs


def get_introduction(bs):
    body_div = bs.find('div', {'id': 'body'})
    sections = body_div.findAll('section')
    intro_sec = None
    for section in sections:
        h2 = section.find('h2')
        little_title = h2.text.lowwer()
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
    sections = body_div.findAll('section')
    conclu_sec = None
    for section in sections:
        h2 = section.find('h2')
        little_title = h2.text.lowwer()
        if 'conclusion' in little_title:
            conclu_sec = section
    conclusion_text = ""
    if not conclu_sec:
        return 'conclusion section do not exist'
    for p in conclu_sec.findAll('p'):
        conclusion_text += p.text
    return conclusion_text


def get_abstract(bs):
    abstract = bs.select('#abstract')
    if abstract:
        return abstract[0].text
    else:
        return ""


def get_en_paper(url, abstract_func, introduction_func, conclusion_func):
    bs = html_bs(url)
    abstract_text = abstract_func(bs)
    introduction_text = introduction_func(bs)
    conclusion_text = conclusion_func(bs)
    return {'abstract_text': abstract_text, 'introduction_text': introduction_text, 'conclusion_text': conclusion_text}


if __name__ == '__main__':
    down_df = pd.read_csv('down_df.csv')
    down_en_df = down_df[down_df['CurDBCode'] == 'SSJD']
    for index, row in down_df.iterrows():
        content_dict = get_en_paper(row['res'], get_abstract, get_introduction, get_conclusion)
        print(content_dict)
