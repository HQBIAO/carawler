# coding=utf-8
# date:上午9:43 
# author:chenjunbiao

import os
import sys

import unittest
import sys

sys.path.append('/home/zengchuan/carawler/')
from crawler.src.wanfang.degree_paper import title_id_pair, save_title_id_pair, get_reference_in_wanfang, \
    get_batch_reference, ref_download_page, down_ref, batch_down_ref
from crawler.src.wanfang.papers import post_json
import pandas as pd


class TestPapers(unittest.TestCase):
    def test_post_json(self):
        self.skipTest('skip')
        param = {'type': 'reference', 'id': 'D01030570', 'number': 1}
        result = post_json('http://www.wanfangdata.com.cn/graphical/turnpage.do', param)
        print result[0][0]['Title']
        print result[1]

    def test_title_ids(self):
        self.skipTest('skip')
        print title_id_pair(1, 1)

    def test_save_ti(self):
        self.skipTest('skip')
        save_title_id_pair(1, 10, 'test.csv')

    def test_get_reference(self):
        self.skipTest('skip')
        # id_title_df = pd.read_csv('id_title')
        paper_id = 'D01030674'
        paper_title = 'paper_title'
        references = get_reference_in_wanfang(paper_id)
        df_references = pd.DataFrame(references)
        df_references['paper_title'] = paper_title
        df_references['paper_id'] = paper_id
        print df_references.columns, df_references['paper_title']

    def test_batch_reference(self):
        self.skipTest('skip')
        id_title_df = pd.read_csv('../degree_paper_with_reference.csv')
        df = get_batch_reference(id_title_df)
        df.to_csv('reference_title.csv', encoding='utf-8', index=False)

    def test_ref_download(self):
        self.skipTest('skip')
        ll = ref_download_page('degree', 'Y2284853')
        down_ref(ll, 'test')

    def test_batch_down_ref(self):
        batch_down_ref()
