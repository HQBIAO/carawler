# coding=utf-8
# date:下午5:14 
# author:chenjunbiao
import unittest

from crawler.src.wanfang.baidu_xueshu import show_page, get_cnki_page, batch_show_page_url


class TestXueshu(unittest.TestCase):
    def test_show_page(self):
        self.skipTest("ship")
        show_page('/s?wd=paperuri%3A%28d33b2c8c45682fc1487f2f7320c218a8%29&filter=sc_long_sign&sc_ks_para=q%3D%E4%B8%8D%E6%88%90%E8%AF%8D%E8%AF%AD%E7%B4%A0%E8%AF%AD%E6%B3%95%E6%80%A7%E7%B1%BB%E9%97%AE%E9%A2%98%E6%8E%A2%E5%BE%AE&sc_us=5696236193743226727&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8')

    def test_get_cnki_page(self):
        self.skipTest("ship")
        get_cnki_page('http://xueshu.baidu.com/usercenter/paper/show?paperid=caea0a249c582d55cff609071c2f8cc2&site=xueshu_se')

    def test_batch_show_page_url(self):
        batch_show_page_url()