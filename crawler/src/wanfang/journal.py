# coding=utf-8
# date:上午9:48 
# author:chenjunbiao
import re
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfdocument import PDFDocument, PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


'''
def create_paper_doc(pdf_path):
    fp = open(pdf_path, 'rb')
    # Create a PDF parser object associated with the file object.
    parser = PDFParser(fp)
    # Create a PDF document object that stores the document structure.
    # Supply the password for initialization.
    document = PDFDocument(parser)
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

    page_count = 0
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        page_text = ""
        for element in layout:
            try:
                print type(element)
            except:
                pass
                # if isinstance(element, LTTextBoxHorizontal):
                #     page_text = page_text + element.get_text()
                # page_text = page_text.strip()
                # page_no = page_text.split('\n')[-1].strip()

                # if re.match(pageno_exp, page_no):
                #     paper_doc.append_page(page_text, page_no)
                #
                # # 查找第一个目录页
                # if re.findall(catalog_exp, page_text) and page_count == 0:
                #     last_index = PaperDoc.find_last_index(page_text, '\n')
                #     paper_doc.catalogtxt = page_text[0:last_index + 1]
                #     page_count += 1
                #     continue
                # # 查找第二个目录页
                # if (paper_doc.catalogtxt and (u'参考文献' not in paper_doc.catalogtxt) and page_count == 1) or \
                #         (paper_doc.catalogtxt and u'参考文献' in paper_doc.catalogtxt and PaperDoc.has_next(
                #             paper_doc.catalogtxt) and page_count == 1):  # 目录页已找到第一页但参考文献条目不在此页，或参考文献条目在此页但是最后一个
                #     paper_doc.catalogtxt += page_text
                #     page_count += 1

    fp.close()'''


def extract_pdf_content(pdf):
    rsrcmgr = PDFResourceManager()
    codec = 'utf-8'
    outfp = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr=rsrcmgr, outfp=outfp, codec=codec, laparams=laparams)
    with open(pdf, 'rb') as fp:
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                      check_extractable=True):
            interpreter.process_page(page)
    mystr = outfp.getvalue()
    device.close()
    outfp.close()
    return mystr


if __name__ == '__main__':
    path = '/Users/chenjunbiao/Downloads/面向人机协同的移动互联网政务门户探析.pdf'
    # create_paper_doc(path)
    print(extract_pdf_content(path))
