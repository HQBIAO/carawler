# coding=utf-8
# date:下午3:08 
# author:chenjunbiao

import os

import pymysql
from pdfminer.layout import LTTextBoxHorizontal
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
import re


class PaperDoc(object):
    def __init__(self):
        self.pages = {}
        self.catalogtxt = None
        self.catalog = []
        self.title = ""
        self.reference_txt = None

    def append_page(self, page_txt, page_no):
        self.pages[page_no] = page_txt

    def get_page_text(self, page_no):
        return self.pages[page_no]

    def analyze_catalog(self):
        if not self.catalogtxt:
            raise Exception('目录文本为空')
        catalog_items = self.catalogtxt.split('\n')
        catalog_items = catalog_items[1:len(catalog_items) - 1]
        for item in catalog_items:
            if len(item)>5:
                reference = re.compile('(\\.+)').split(item)
                # print reference
                self.catalog.append(reference)

    @staticmethod
    def __page_no_str(string):
        no = ""
        for ch in string:
            if ch >= '0' and ch <= '9':
                no += ch
        return no

    def extract_reference(self):
        self.analyze_catalog()
        if not self.catalog:
            return None
        summary_page_no = 0
        next_of_summary_page_no = 0
        re_digit = re.compile('[1-9]\d*')
        for index in range(len(self.catalog)):
            if u'参考文献' in self.catalog[index][0]:
                # summary_index = index
                try:
                    summary_page_no = int(PaperDoc.__page_no_str(self.catalog[index][-1]))
                    next_of_summary_page_no = int(PaperDoc.__page_no_str(self.catalog[index + 1][-1]))
                    break
                except ValueError as e:
                    print self.title, summary_page_no
                    print e

        reference_text = u""
        for page_no in range(summary_page_no, next_of_summary_page_no):
            reference_text = reference_text + self.pages[str(page_no)]
        self.reference_txt = reference_text

        i = reference_text.index(u'参考文献')
        reference_text = reference_text[i:len(reference_text)]
        reference_items = re.compile('(\\[[1-9][0-9]*\\])').split(reference_text)
        reference_items = [item for item in reference_items[1:len(reference_items)] if len(item) > 5]
        return reference_items

    @staticmethod
    def create_paper_doc(pdf_path):
        # fp = open('/Users/chenjunbiao/project/graduation_project/data/菲律宾无多媒体环境下教师板书调查研究.pdf', 'rb')
        fp = open(pdf_path, 'rb')
        # Create a PDF parser object associated with the file object.
        parser = PDFParser(fp)
        # Create a PDF document object that stores the document structure.
        # Supply the password for initialization.
        document = PDFDocument(parser, "")
        # Check if the document allows text extraction. If not, abort.
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed
        # Create a PDF resource manager object that stores shared resources.
        rsrcmgr = PDFResourceManager()
        from pdfminer.layout import LAParams
        from pdfminer.converter import PDFPageAggregator

        # Set parameters for analysis.
        laparams = LAParams()
        # Create a PDF page aggregator object.
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        paper_doc = PaperDoc()
        paper_doc.title = pdf_path.split('/')[-1].split('.')[0]
        pageno_exp = u'^I|(\+?[1-9][0-9]*)'
        catalog_exp = u'(目录)|(目\s+录)'

        page_count = 0
        for page in PDFPage.create_pages(document):
            interpreter.process_page(page)
            layout = device.get_result()
            page_text = ""
            for element in layout:
                if isinstance(element, LTTextBoxHorizontal):
                    page_text = page_text + element.get_text()
            page_text = page_text.strip()
            page_no = page_text.split('\n')[-1].strip()

            if re.match(pageno_exp, page_no):
                paper_doc.append_page(page_text, page_no)

            # 查找第一个目录页
            if re.findall(catalog_exp, page_text) and page_count == 0:
                last_index = PaperDoc.find_last_index(page_text, '\n')
                paper_doc.catalogtxt = page_text[0:last_index+1]
                page_count += 1
                continue
            # 查找第二个目录页
            if (paper_doc.catalogtxt and (u'参考文献' not in paper_doc.catalogtxt) and page_count == 1) or \
                    (paper_doc.catalogtxt and u'参考文献' in paper_doc.catalogtxt and PaperDoc.has_next(
                        paper_doc.catalogtxt) and page_count == 1):  # 目录页已找到第一页但参考文献条目不在此页，或参考文献条目在此页但是最后一个
                paper_doc.catalogtxt += page_text
                page_count += 1

        fp.close()
        return paper_doc

    @staticmethod
    def has_next(text):
        ll = text.split('\n')
        for i in range(len(ll)):
            if u'参考文献' in ll[i]:
                break
        if not re.findall('(\\.+)', ll[i + 1]):
            return True
        else:
            return False

    @staticmethod
    def find_last_index(p_str, m_str):
        for i in range(len(p_str) - 1, -1, -1):
            if p_str[i] == m_str:
                return i
        return -1


class Mysql(object):
    def __init__(self, host="", password="", database='', user=''):
        self.host = host
        self.password = password
        self.database = database
        self.user = user
        self.charset = 'utf8'
        self.db = None
        self.cursor = None

    def __del__(self):
        self.db.close()

    def connect(self):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset=self.charset)
        self.cursor = self.db.cursor()

    def insert(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()


''' from pdfminer.layout import LAParams
    from pdfminer.converter import PDFPageAggregator

    # Set parameters for analysis.
    laparams = LAParams()
    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    paper_doc = PaperDoc()
    pageno_exp = u'^I|(\+?[1-9][0-9]*)'
    catalog_exp = u'^目\s{2,}录'

    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        page_text = ""
        for element in layout:
            if isinstance(element, LTTextBoxHorizontal):
                page_text = page_text + element.get_text()
        page_text = page_text.strip()
        page_no = page_text[-3:].strip()
        if re.match(pageno_exp, page_no):
            paper_doc.append_page(page_text, page_no)
        if re.findall(catalog_exp, page_text):
            paper_doc.catalogtxt = page_text
    return paper_doc
# Create a PDF device object.
def parse_pdf():
    device = PDFDevice(rsrcmgr)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.
    pages = PDFPage.create_pages(document)
    i = 0
    for page in pages:
        i += 1
        print i
        print interpreter.process_page(page)
        print page


def analysis_layout():
    from pdfminer.layout import LAParams
    from pdfminer.converter import PDFPageAggregator

    # Set parameters for analysis.
    laparams = LAParams()
    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    paper_doc = PaperDoc()
    pageno_exp = u'^I|(\+?[1-9][0-9]*)'
    catalog_exp = u'^目\s{2,}录'

    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        page_text = ""
        for element in layout:
            if isinstance(element, LTTextBoxHorizontal):
                page_text = page_text + element.get_text()
        page_text = page_text.strip()
        page_no = page_text[-3:].strip()
        if re.match(pageno_exp, page_no):
            paper_doc.append_page(page_text, page_no)
        if re.findall(catalog_exp, page_text):
            paper_doc.catalogtxt = page_text
    return paper_doc'''


def spilt_reference(reference_item):
    reference_dic = {}
    reference_dic['author'] = reference_item[0]

    reference_dic['source'] = reference_item[2]
    reference_info = reference_item[1].split('[')
    reference_type = reference_info[1][0]
    reference_title = reference_info[0]
    reference_dic['reference_title'] = reference_title
    reference_dic['reference_type'] = reference_type
    return reference_dic


def get_ref_txt():
    dir_path = '/Users/chenjunbiao/project/graduation_project/data1/'
    file_name_list = os.listdir(dir_path)
    mysql = Mysql()
    mysql.connect()
    for file_name in file_name_list:
        try:
            if file_name == '.DS_Store':
                continue
            file_path = dir_path + file_name
            paper_doc = PaperDoc.create_paper_doc(file_path)
            paper_doc.extract_reference()
            reftxt = paper_doc.reference_txt
            sql = "INSERT INTO reference_copy_copy(paper_title, ref_txt) VALUES ('%s',  '%s' )" % \
                  (paper_doc.title, reftxt.encode('utf-8'))
            mysql.insert(sql)
        except BaseException as e:
            print paper_doc.title + "   参考文本获取失败"
            print e


if __name__ == '__main__':

    dir_path = '/Users/chenjunbiao/project/graduation_project/data/'
    file_name_list = os.listdir(dir_path)

    mysql = Mysql()
    mysql.connect()

    for file_name in file_name_list:
        try:
            if file_name == '.DS_Store':
                continue
            file_path = dir_path + file_name
            paper_doc = PaperDoc.create_paper_doc(file_path)
            reference_items = paper_doc.extract_reference()

            for item in reference_items:
                # reference_dic = spilt_reference(item)
                # sql = "INSERT INTO reference(paper_title, \
                #        author, reference_title,source, type, getted) \
                #        VALUES ('%s', '%s', '%s', '%s','%s', '%d' )" % \
                #       (paper_doc.title, reference_dic['author'].encode('utf-8'),
                #        reference_dic['reference_title'].encode('utf-8'),
                #        reference_dic['source'].encode('utf-8'), reference_dic['reference_type'].encode('utf-8'),
                #        0)
                sql = "INSERT INTO reference_copy(paper_title, reference_title, getted) \
                                       VALUES ('%s', '%s', '%d' )" % \
                      (paper_doc.title, item.encode('utf-8'), 0)
                mysql.insert(sql)
        except BaseException as e:
            print file_name + "  参考文献提取失败"
            print e
