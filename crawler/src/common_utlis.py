# coding=utf-8
# date:下午1:51
# author:chenjunbiao
import glob
import re
from pathlib import Path
import pandas as pd


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
        '/error_files.csv', index=False)
    # with open('../error_files.txt','w') as f:
    #     for name in name_list:
    #         f.write(name[0]+'\t'+name[1]+'\t'+name[2]+'\n')
    # this can work too
    # files = glob.glob(str(Path.home().joinpath('j_ref')) + '/**/*.caj', recursive=True)
    # print(files)


if __name__ == '__main__':
    get_error_file()
    """
    p = str(Path.cwd().joinpath('《全漢志傳》雙音動詞研究-------《<後漢書>雙音動詞研究》.caj'))
    # p = str(Path.cwd().joinpath('dd.caj'))
    with open(p,'wb') as f:
        f.write('fdkjfjk'.encode('utf-8'))
"""