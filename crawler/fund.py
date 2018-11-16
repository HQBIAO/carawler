import requests
import execjs
import time
from openpyxl import Workbook
from bs4 import BeautifulSoup


def get_fund_list(page):
    '''获取基金列表,page表示页码'''
    print('获取第' + str(page) + "页股票基金-----------------------------------------")
    url = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=gp&rs=&gs=0&sc=zzf&st=desc&sd=2017-03-22&ed=2018-03-22&qdii=&tabSubtype=,,,,,&pi={}&pn=50&dx=1&v=0.6878808497956146'
    headers ={'user-agent': 'my-app/0.0.1'}
    response = requests.get(url.replace('{}', str(page)),headers=headers)
    print(response.request.headers)
    json_str = response.text
    result_dict = execjs.eval(json_str.lstrip('var rankData = ').rstrip(';'))
    fund_list = result_dict['datas']
    return fund_list


def get_fund_holdings(fund_code, fund_name):
    '''获取基金的股票持仓数据，fund_code:基金代码，fund_name：基金名称'''
    url = 'http://fund.eastmoney.com/f10/FundArchivesDatas.aspx?type=jjcc&code={}&topline=10&year=&month=&rt=0.3268956984799769'
    url = url.replace('{}', str(fund_code))
    print("持仓信息,基金代码:" + str(fund_code) + "；基金名称:" + fund_name + "；获取持仓数据链接:" + url)
    response = requests.get(url)
    json_str = response.text.lstrip('var apidata=').rstrip(';')
    result_dict = execjs.eval(json_str)
    # if result_dict['content']:
    #     return []
    soup = BeautifulSoup(result_dict['content'], 'html.parser')
    tbody_tags = soup.select('tbody')
    tr_tags = tbody_tags[0].findChildren('tr')
    stock_holdings = []
    for tr_tag in tr_tags:
        stock_info = {}
        a_tags = tr_tag.select('td a')
        stock_code = a_tags[0].text
        stock_name = a_tags[1].text
        holding_proportion = tr_tag.select('.tor')[-3].text
        stock_info['stock_code'] = stock_code
        stock_info['stock_name'] = stock_name
        stock_info['holding_proportion'] = holding_proportion
        stock_holdings.append(stock_info)
    return stock_holdings


def write_fund_info(fund_code, fund_name, stock_holdings, work_book):
    '''将数据写入excel文件；fund_code:基金代码，fund_name：基金名称，stock_holdings：基金对应的持仓数据，work_book:excel文件对象'''
    ws = work_book.active
    for stock in stock_holdings:
        ws.append([fund_code, fund_name, stock['stock_code'], stock['stock_name'], stock['holding_proportion']])
    return work_book


if __name__ == '__main__':
    '''建立一个excel工作簿对象'''
    work_book = Workbook()

    for i in range(1, 2):
        fund_list = []
        try:
            fund_list = get_fund_list(i)
        except BaseException:
            print("基金信息获取失败", BaseException.__traceback__)
        if fund_list:
            for fund in fund_list:
                array = fund.split(',')
                code = array[0]
                name = array[1]
                stock_holdings = []
                # stock_holdings = get_fund_holdings(code, name)
                try:
                    stock_holdings = get_fund_holdings(code, name)
                except IndexError:
                    print('持仓信息获取失败:无持仓数据')
                    print(code,name)
                time.sleep(1)  # 让程序停顿1秒
                work_book = write_fund_info(code, name, stock_holdings, work_book)
        time.sleep(2)  # 让程序停顿2秒
        # work_book.save("基金.xlsx")
