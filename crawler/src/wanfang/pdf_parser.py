# coding=utf-8
# date:下午1:56 
# author:chenjunbiao
# from pdfminer.pdfparser import PDFParser, PDFDocument
import sys
from pdfminer.cmapdb import CMapDB
from pdfminer.image import ImageWriter
from pdfminer.pdfdevice import TagExtractor
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator, TextConverter, XMLConverter, HTMLConverter
from pdfminer.layout import LTTextBoxHorizontal, LAParams
# from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

# path = r'/Users/chenjunbiao/project/毕业设计/data/chapter1.pdf'
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

path = r'/Users/chenjunbiao/project/graduation_project/data/透明度对中高级水平在华留学生汉语惯用语理解的影响.pdf'


# def parse():
#     fp = open(path, 'rb')  # 以二进制读模式打开
#     # 用文件对象来创建一个pdf文档分析器
#     praser = PDFParser(fp)
#     # 创建一个PDF文档
#     doc = PDFDocument()
#     # 连接分析器 与文档对象
#     praser.set_document(doc)
#     doc.set_parser(praser)
#
#     # 提供初始化密码
#     # 如果没有密码 就创建一个空的字符串
#     # doc.initialize()
#
#     # 检测文档是否提供txt转换，不提供就忽略
#     rsrcmgr = PDFResourceManager()
#     # 创建一个PDF设备对象
#     laparams = LAParams()
#     device = PDFPageAggregator(rsrcmgr, laparams=laparams)
#     # 创建一个PDF解释器对象
#     interpreter = PDFPageInterpreter(rsrcmgr, device)
#
#     # 循环遍历列表，每次处理一个page的内容
#     for page in doc.get_pages():  # doc.get_pages() 获取page列表
#         interpreter.process_page(page)
#         # 接受该页面的LTPage对象
#         layout = device.get_result()
#         # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
#         for x in layout:
#             if (isinstance(x, LTTextBoxHorizontal)):
#                 with open(r'./1.txt', 'a') as f:
#                     results = x.get_text()
#                     print(results)
#                     f.write(results + '\n')
def main():
    # print argv
    # import getopt
    # def usage():
    #     print ('usage: %s [-d] [-p pagenos] [-m maxpages] [-P password] [-o output]'
    #            ' [-C] [-n] [-A] [-V] [-M char_margin] [-L line_margin] [-W word_margin]'
    #            ' [-F boxes_flow] [-Y layout_mode] [-O output_dir] [-R rotation] [-S]'
    #            ' [-t text|html|xml|tag] [-c codec] [-s scale]'
    #            ' file ...' % argv[0])
    #     return 100
    # try:
    #     (opts, args) = getopt.getopt(argv[1:], 'dp:m:P:o:CnAVM:L:W:F:Y:O:R:St:c:s:')
    # except getopt.GetoptError:
    #     return usage()
    # if not args: return usage()
    # # debug option
    # debug = 0
    # # input option
    password = ''
    pagenos = set()
    maxpages = 0
    # # output option
    # outfile = None
    outtype = None
    imagewriter = None
    rotation = 0
    stripcontrol = False
    layoutmode = 'normal'
    codec = 'utf-8'
    pageno = 1
    scale = 1
    caching = True
    # showpaeno = True
    laparams = LAParams()
    debug=1
    PDFDocument.debug = debug
    PDFParser.debug = debug
    CMapDB.debug = debug
    PDFPageInterpreter.debug = debug

    rsrcmgr = PDFResourceManager(caching=caching)
    outfile=r'/Users/chenjunbiao/project/graduation_project/data/xmlout.xml'
    if not outtype:
        outtype = 'text'
        if outfile:
            if outfile.endswith('.htm') or outfile.endswith('.html'):
                outtype = 'html'
            elif outfile.endswith('.xml'):
                outtype = 'xml'
            elif outfile.endswith('.tag'):
                outtype = 'tag'
    if outfile:
        outfp = file(outfile, 'w')
    else:
        outfp = sys.stdout
    if outtype == 'text':
        device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                               imagewriter=imagewriter)
    elif outtype == 'xml':
        device = XMLConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                              imagewriter=imagewriter,
                              stripcontrol=stripcontrol)
    elif outtype == 'html':
        device = HTMLConverter(rsrcmgr, outfp, codec=codec, scale=scale,
                               layoutmode=layoutmode, laparams=laparams,
                               imagewriter=imagewriter, debug=debug)
    elif outtype == 'tag':
        device = TagExtractor(rsrcmgr, outfp, codec=codec)
    else:
        return
    # for fname in args:
    #     fp = file(fname, 'rb')
    #     interpreter = PDFPageInterpreter(rsrcmgr, device)
    #     for page in PDFPage.get_pages(fp, pagenos,
    #                                   maxpages=maxpages, password=password,
    #                                   caching=caching, check_extractable=True):
    #         page.rotate = (page.rotate+rotation) % 360
    #         interpreter.process_page(page)
    #     fp.close()
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(fp, pagenos,
                                  maxpages=maxpages, password=password,
                                  caching=caching, check_extractable=True):
        page.rotate = (page.rotate + rotation) % 360
        interpreter.process_page(page)
    fp.close()
    device.close()
    outfp.close()
    return


if __name__ == "__main__":
    main()