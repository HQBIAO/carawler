# coding=utf-8
# date:下午1:51
# author:chenjunbiao
import glob
import re
from pathlib import Path


def filter_chi_char(s):
    s = re.findall('[\u4e00-\u9fa5]', s)
    return ''.join(str(e) for e in s)


def filter_file_by_size():
    result = list(Path.home().joinpath('j_ref').rglob("*.caj"))
    for r in result:
        size = r.stat().st_size / 1024
        if size<15:
            print(r.name, size)


if __name__ == '__main__':
    filter_file_by_size()

    # this can work too
    # files = glob.glob(str(Path.home().joinpath('j_ref')) + '/**/*.caj', recursive=True)
    # print(files)
