# coding=utf-8
# date:2019/2/1 下午7:45 
# author:chenjunbiao
import platform
from pathlib import Path

import pandas as pd
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


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


def get_wiley_abstract(bs):
    abstract = bs.select('.abstract-group')
    if abstract:
        return abstract[0].text
    else:
        return ""


def get_wiley_introduction(bs):
    sections = bs.select('.article-section_content')
    if not sections:
        return 'body do not exist'
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


def get_wiley_conclusion(bs):
    sections = bs.select('.article-section_content')
    if not sections:
        return 'body do not exist'
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


def get_en_paper(url, abstract_func, introduction_func, conclusion_func):
    # capa = DesiredCapabilities.CHROME
    # capa["pageLoadStrategy"] = "none"

    if platform.system() == 'Windows':
        driver = webdriver.Chrome(r'C:\Users\lvzen\Downloads\chromedriver_win32 (1)\chromedriver.exe')
        # driver = webdriver.Chrome(r'C:\Users\lvzen\AppData\Local\Google\Chrome\Application\chromedriver.exe')
        # driver = webdriver.PhantomJS(executable_path=r'C:\Users\lvzen\Downloads\kk\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    else:
        driver = webdriver.Chrome()
    # wait = WebDriverWait(driver,40)
    try:
        driver.get(url)
        driver.implicitly_wait(30)
        # wait.until(EC.presence_of_all_elements_located(By.CSS_SELECTOR,'#body'))
        # driver.execute_script('window.stop();')
        # page_source = driver.page_source
    except TimeoutException:
        driver.close()
        return None
        # print('js stop begin')
        # driver.execute_script("window.stop()")
        # driver.execute_script("window.stop('dd')")
        # driver.find_element_by_id('kw').send_keys(Keys.ESCAPE)
        # print('js stop end')
        # page_source = driver.page_source
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
        if 'sciencedirect' in row['res']:
            save_path = Path.home().joinpath('sciencedirect', row['target_paper'])
            if not save_path.exists():
                save_path.mkdir(parents=True)
            if save_path.joinpath(row['uuid'] + '.txt').is_file():
                print(save_path.joinpath(row['uuid'] + '.txt'), 'already exist')
                continue
            content_dict = get_en_paper(row['res'], get_abstract, get_introduction, get_conclusion)
            if content_dict:
                with open(str(save_path.joinpath(row['uuid'] + '.txt')), 'w', encoding='utf-8') as f:
                    f.write('abstract\n')
                    f.write(content_dict['abstract_text'] + '\n')
                    f.write('introduction\n')
                    f.write(content_dict['introduction_text'] + '\n')
                    f.write('conclusion\n')
                    f.write(content_dict['conclusion_text'] + '\n')
            else:
                print(row['uuid'], '超时')
        if 'wiley' in row['res']:
            save_path = Path.home().joinpath('wiley', row['target_paper'])
            if not save_path.exists():
                save_path.mkdir(parents=True)
            if save_path.joinpath(row['uuid'] + '.txt').is_file():
                print(save_path.joinpath(row['uuid'] + '.txt'), 'already exist')
                continue
            content_dict = get_en_paper(row['res'], get_wiley_abstract, get_wiley_introduction, get_wiley_conclusion)
            if content_dict:
                with open(str(save_path.joinpath(row['uuid'] + '.txt')), 'w', encoding='utf-8') as f:
                    f.write('abstract\n')
                    f.write(content_dict['abstract_text'] + '\n')
                    f.write('introduction\n')
                    f.write(content_dict['introduction_text'] + '\n')
                    f.write('conclusion\n')
                    f.write(content_dict['conclusion_text'] + '\n')
            else:
                print(row['uuid'], '超时')
