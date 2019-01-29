# coding=utf-8
# date:下午1:51
# author:chenjunbiao
import glob
import re
from pathlib import Path
import pandas as pd
import shutil


def filter_chi_char(s):
    s = re.findall('[\u4e00-\u9fa5]', s)
    return ''.join(str(e) for e in s)


def filter_file_by_size(ref_type):
    name_list = []
    result = list(Path.home().joinpath(ref_type).rglob("*.caj"))
    for r in result:
        size = r.stat().st_size / 1024
        if size < 15:
            name_list.append((r.parent.name, r.stem, size))
    return name_list


def get_error_file():
    _list = []
    _list.extend(filter_file_by_size('cnki'))
    # _list.extend(filter_file_by_size('j_ref'))
    # _list.extend(filter_file_by_size('d_ref'))
    # _list.extend(filter_file_by_size('c_ref'))
    paper_title_list = [name[0] for name in _list]
    title_list = [name[1] for name in _list]
    size_list = [name[2] for name in _list]
    pd.DataFrame({'paper_title': paper_title_list, 'title': title_list, 'size_kb': size_list}).to_csv(
        'error_files.csv', index=False)
    # with open('../error_files.txt','w') as f:
    #     for name in name_list:
    #         f.write(name[0]+'\t'+name[1]+'\t'+name[2]+'\n')
    # this can work too
    # files = glob.glob(str(Path.home().joinpath('j_ref')) + '/**/*.caj', recursive=True)
    # print(files)


def get_papers_has_ref():
    papers = pd.read_csv('/Users/chenjunbiao/project/graduation_project/paper_degree_paper_with_reference.csv')
    paper_list = list(papers['paper_title'])
    for pdf in Path('/Users/chenjunbiao/project/graduation_project/data1').rglob("*.pdf"):
        if pdf.stem in paper_list:
            try:
                shutil.move(str(pdf), '/Users/chenjunbiao/project/graduation_project/degree_paper')
            except:
                pass


def batch_create_txt():
    for docx in Path('/Users/chenjunbiao/Desktop/target_paper').rglob("*.docx"):
        if 'Pdf' in docx.stem:
            continue
        with open(str(docx.parent.joinpath(docx.stem + '.txt')), 'w') as f:
            f.write('')


def get_downloaded_list():
    name_list = []
    result = list(Path.home().joinpath('cnki').rglob("*.caj"))
    for r in result:
        name_list.append((r.parent.name, r.stem, r.stat().st_size / 1024))
    pd.DataFrame(columns={'paper_title', 'title', 'size'}, data=name_list).to_csv('downloaded_files.csv', index=False)


def find_all_file_recursively(dir_path, suffix):
    return Path(dir_path).rglob('*' + suffix)


def regulate_name():
    for p in Path('/Users/chenjunbiao/Desktop/train_data/ref_paper/').rglob('*.caj*'):
        # print(p)
        # print(p.stem.split('.caj')[0])
        stem = p.stem.split('.caj')[0]
        print(stem)
        shutil.move(str(p), str(p.with_name(stem + p.suffix)))


if __name__ == '__main__':
    # get_error_file()
    """
    p = str(Path.cwd().joinpath('《全漢志傳》雙音動詞研究-------《<後漢書>雙音動詞研究》.caj'))
    # p = str(Path.cwd().joinpath('dd.caj'))
    with open(p,'wb') as f:
        f.write('fdkjfjk'.encode('utf-8'))
"""
    # get_papers_has_ref()
    # batch_create_txt()
    # get_downloaded_list()
    regulate_name()
