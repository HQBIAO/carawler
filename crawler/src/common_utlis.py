# coding=utf-8
# date:下午1:51
# author:chenjunbiao
import re


def filter_chi_char(s):
    s = re.findall('[\u4e00-\u9fa5]', s)
    return ''.join(str(e) for e in s)
