# coding=utf-8
# date:2019/1/28 上午1:26
# author:chenjunbiao
import unittest
import pandas as pd

from crawler.src.wanfang.download_cnki import get_ref_list, get_down_url


class TestCnki(unittest.TestCase):
    def test_get_ref_list(self):
        self.skipTest('')
        # get_ref_list('/kns/detail/detail.aspx?dbcode=CMFD&QueryID=29&CurRec=6&dbname=CMFD201802&filename=1018887591.nh',
        #              "")
        ref_df = pd.DataFrame(columns=['target_paper', 'ref_href', 'ref_title', 'text', 'CurDBCode'])
        with open('/Users/chenjunbiao/project/graduation_project/金融学科数据集/detail_url.txt', 'r') as f:
            lines = f.readlines()
        for i in range(0, len(lines), 2):
            url = lines[i].split()[1].strip()
            target_paper = lines[i + 1].split()[1].strip()
            ref_df = ref_df.append(get_ref_list(url, target_paper))
        ref_df.to_csv('金融参考文献.csv', index=False)

    def test_get_down_url(self):
        self.skipTest("")
        ref_df = pd.read_csv('金融参考文献.csv')
        ref_df['down_link'] = ref_df.apply(
            lambda x: get_down_url(x['ref_href'], x['CurDBCode']), axis=1)
        ref_df.to_csv('金融参考文献_down.csv', index=False)

    def test_name(self):
        # \、 / 、:、 * 、?、"、<、>、|
        # print('rr\\a/l:*?"|')
        # print(
        #     'rr\\a/l:*?"|'.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?',
        #                                                                                                 '').replace(
        #         '"', '').replace('|', '').replace('<', '').replace('>', ''))

        def replace_ch(str1):
            if isinstance(str1, str):
                return str1.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?',
                                                                                                         '').replace(
                    '"', '').replace('|', '').replace('<', '').replace('>', '')
            else:
                return str1

        down_df = pd.read_csv('/Users/chenjunbiao/project/carawler/crawler/src/wanfang/down_df.csv')
        down_df['ref_title'] = down_df.apply(
            lambda x: replace_ch(x['ref_title']), axis=1)
        down_df.to_csv('/Users/chenjunbiao/project/carawler/crawler/src/wanfang/down_df.csv')
