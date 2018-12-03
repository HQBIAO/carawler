# -*- coding: utf-8 -*-
# @Time    : 2018/3/1 21:03
# @Author  : stephenfeng
# @Software: PyCharm Community Edition

'''
帮思月 爬取股票信息
'''

s = """
<dl id="content_cp" class="dl-guide-comm">
  <dd id="cp_c_def" class="defc" style="display:none;"></dd>
  <dd id="cp_c_hot" style="display: none;">
    <a id="cp_80000222_hot" name="click">华夏</a>
    <a id="cp_80000223_hot" name="click">嘉实</a>
    <a id="cp_80000229_hot" name="click">易方达</a>
    <a id="cp_80000220_hot" name="click">南方</a>
    <a id="cp_80048752_hot" name="click">中银</a>
    <a id="cp_80000248_hot" name="click">广发</a>
    <a id="cp_80064225_hot" name="click">工银</a>
    <a id="cp_80000226_hot" name="click">博时</a>
    <a id="cp_80000228_hot" name="click">华安</a>
    <a class="last " id="cp_80053708" name="click">汇添富</a></dd>
  <dd id="cp_c_A" style="display:none;">
    <a class="last" id="cp_80163340" name="click">安信</a></dd>
  <dd id="cp_c_B" style="display:none;">
    <a id="cp_80560392" name="click">博道</a>
    <a id="cp_80538609" name="click">渤海汇金</a>
    <a id="cp_80000226" name="click">博时</a>
    <a id="cp_80365985" name="click">北信瑞丰</a>
    <a class="last" id="cp_80000236" name="click">宝盈</a></dd>
  <dd id="cp_c_C" style="display:none;">
    <a id="cp_80139382" name="click">长安</a>
    <a id="cp_80000239" name="click">长城</a>
    <a id="cp_80380794" name="click">创金合信</a>
    <a id="cp_80404004" name="click">长江证券(上海)</a>
    <a id="cp_80000227" name="click">长盛</a>
    <a id="cp_80161341" name="click">财通</a>
    <a id="cp_80404701" name="click">财通资管</a>
    <a class="last" id="cp_80000243" name="click">长信</a></dd>
  <dd id="cp_c_D" style="display:none;">
    <a id="cp_80175511" name="click">德邦</a>
    <a id="cp_80000225" name="click">大成</a>
    <a id="cp_80560388" name="click">东方阿尔法</a>
    <a id="cp_80042861" name="click">东方</a>
    <a id="cp_80205268" name="click">东海</a>
    <a id="cp_80048161" name="click">东吴</a>
    <a class="last" id="cp_80114781" name="click">东兴证券</a></dd>
  <dd id="cp_c_F" style="display:none;">
    <a id="cp_80128562" name="click">富安达</a>
    <a id="cp_80000221" name="click">富国</a>
    <a id="cp_80488954" name="click">富荣</a>
    <a class="last" id="cp_80174741" name="click">方正富邦</a></dd>
  <dd id="cp_c_G" style="display:none;">
    <a id="cp_80048088" name="click">光大保德信</a>
    <a id="cp_80000095" name="click">国都证券</a>
    <a id="cp_80000248" name="click">广发</a>
    <a id="cp_80044515" name="click">国海富兰克林</a>
    <a id="cp_80056613" name="click">高华证券</a>
    <a id="cp_80102419" name="click">国金</a>
    <a id="cp_80280039" name="click">国开泰富</a>
    <a id="cp_80043374" name="click">国联安</a>
    <a id="cp_80548351" name="click">格林</a>
    <a id="cp_80560389" name="click">国融</a>
    <a id="cp_80355783" name="click">国寿安保</a>
    <a id="cp_80000224" name="click">国泰</a>
    <a id="cp_80000233" name="click">国投瑞银</a>
    <a class="last" id="cp_80064225" name="click">工银瑞信</a></dd>
  <dd id="cp_c_H" style="display:none;">
    <a id="cp_80000228" name="click">华安</a>
    <a id="cp_80498278" name="click">汇安</a>
    <a id="cp_80000250" name="click">华宝</a>
    <a id="cp_80201857" name="click">华宸未来</a>
    <a id="cp_80424273" name="click">泓德</a>
    <a id="cp_80037023" name="click">华富</a>
    <a id="cp_80067635" name="click">汇丰晋信</a>
    <a id="cp_80000246" name="click">海富通</a>
    <a id="cp_80199117" name="click">华润元大</a>
    <a id="cp_80092743" name="click">华融证券</a>
    <a id="cp_80053204" name="click">华商</a>
    <a id="cp_80508384" name="click">恒生前海</a>
    <a id="cp_80055334" name="click">华泰柏瑞</a>
    <a id="cp_80523667" name="click">华泰保兴</a>
    <a id="cp_80385906" name="click">红土创新</a>
    <a id="cp_80053708" name="click">汇添富</a>
    <a id="cp_80205263" name="click">红塔红土</a>
    <a id="cp_80391977" name="click">华泰证券(上海)</a>
    <a id="cp_80000222" name="click">华夏</a>
    <a id="cp_80560380" name="click">恒越</a>
    <a class="last" id="cp_80560379" name="click">弘毅远方</a></dd>
  <dd id="cp_c_J" style="display:none;">
    <a id="cp_80365987" name="click">嘉合</a>
    <a id="cp_80000251" name="click">景顺长城</a>
    <a id="cp_80000223" name="click">嘉实</a>
    <a id="cp_80384640" name="click">九泰</a>
    <a id="cp_80065990" name="click">建信</a>
    <a id="cp_80205264" name="click">江信</a>
    <a id="cp_80446423" name="click">金信</a>
    <a id="cp_80000245" name="click">金鹰</a>
    <a id="cp_80086876" name="click">金元顺安</a>
    <a class="last" id="cp_80064562" name="click">交银施罗德</a></dd>
  <dd id="cp_c_K" style="display:none;">
    <a class="last" id="cp_80560381" name="click">凯石</a></dd>
  <dd id="cp_c_M" style="display:none;">
    <a id="cp_80036797" name="click">摩根士丹利华鑫</a>
    <a class="last" id="cp_80106677" name="click">民生加银</a></dd>
  <dd id="cp_c_N" style="display:none;">
    <a id="cp_80049689" name="click">诺安</a>
    <a id="cp_80068180" name="click">诺德</a>
    <a id="cp_80000220" name="click">南方</a>
    <a id="cp_80555446" name="click">南华</a>
    <a class="last" id="cp_80092233" name="click">农银汇理</a></dd>
  <dd id="cp_c_P" style="display:none;">
    <a id="cp_80168726" name="click">平安大华</a>
    <a id="cp_80000230" name="click">鹏华</a>
    <a id="cp_80091787" name="click">浦银安盛</a>
    <a class="last" id="cp_80522693" name="click">鹏扬</a></dd>
  <dd id="cp_c_Q" style="display:none;">
    <a id="cp_80280038" name="click">前海开源</a>
    <a id="cp_80468996" name="click">前海联合</a>
    <a class="last" id="cp_80560396" name="click">青松</a></dd>
  <dd id="cp_c_R" style="display:none;">
    <a id="cp_80061431" name="click">人保资产</a>
    <a class="last" id="cp_80000231" name="click">融通</a></dd>
  <dd id="cp_c_S" style="display:none;">
    <a id="cp_80145102" name="click">上海东方证券资产管理</a>
    <a id="cp_80050229" name="click">上投摩根</a>
    <a id="cp_80045188" name="click">申万菱信</a>
    <a id="cp_80000080" name="click">山西证券</a>
    <a class="last" id="cp_80366080" name="click">上银</a></dd>
  <dd id="cp_c_T" style="display:none;">
    <a id="cp_80000238" name="click">泰达宏利</a>
    <a id="cp_80041198" name="click">天弘</a>
    <a id="cp_80061674" name="click">泰康资产</a>
    <a id="cp_80294346" name="click">太平</a>
    <a id="cp_80000247" name="click">泰信</a>
    <a class="last" id="cp_80000252" name="click">天治</a></dd>
  <dd id="cp_c_W" style="display:none;">
    <a class="last" id="cp_80000240" name="click">万家</a></dd>
  <dd id="cp_c_X" style="display:none;">
    <a id="cp_80147736" name="click">西部利得</a>
    <a id="cp_80074234" name="click">信达澳银</a>
    <a id="cp_80501166" name="click">先锋</a>
    <a id="cp_80000249" name="click">新华</a>
    <a id="cp_80036742" name="click">兴全</a>
    <a id="cp_80452130" name="click">新沃</a>
    <a id="cp_80351991" name="click">鑫元</a>
    <a id="cp_80280395" name="click">兴业</a>
    <a class="last" id="cp_80368700" name="click">兴银</a></dd>
  <dd id="cp_c_Y" style="display:none;">
    <a id="cp_80175498" name="click">英大</a>
    <a id="cp_80000229" name="click">易方达</a>
    <a id="cp_80000235" name="click">银华</a>
    <a id="cp_80000237" name="click">银河</a>
    <a id="cp_80046522" name="click">益民</a>
    <a id="cp_80280036" name="click">圆信永丰</a>
    <a class="last" id="cp_80356155" name="click">永赢</a></dd>
  <dd id="cp_c_Z" style="display: block;">
    <a id="cp_80046614" name="click" class=" at">中海</a>
    <a id="cp_80508391" name="click" class="">中航</a>
    <a id="cp_80351345" name="click" class="">中加</a>
    <a id="cp_80365986" name="click" class="">中金</a>
    <a id="cp_80455765" name="click">中科沃土</a>
    <a id="cp_80065113" name="click" class="">中欧</a>
    <a id="cp_80341238" name="click" class="">中融</a>
    <a id="cp_80156777" name="click">浙商</a>
    <a id="cp_80036782" name="click">招商</a>
    <a id="cp_80403111" name="click">浙商证券资管</a>
    <a id="cp_80066470" name="click">中信保诚</a>
    <a id="cp_80355113" name="click" class="">中信建投</a>
    <a id="cp_80000200" name="click">中银国际证券</a>
    <a id="cp_80075936" name="click" class="">中邮</a>
    <a class="last" id="cp_80048752" name="click">中银</a></dd>
</dl>
"""

from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
import time

# 获取每个基金公司的代号  eg：华夏对应80000222
soup = BeautifulSoup(str(s), "html.parser")
element = soup.find_all('dd', {'style':"display:none;"})
resultList = []
for blocks in element:
    for block in blocks.find_all('a'):
        try:
            resultList.append([block.get('id')[3:], block.get_text()])
            print(block.get('id')[3:], block.get_text())
        except:pass
resultList = pd.DataFrame(resultList, columns=['id','name'])


aimUrl_start = 'http://fund.eastmoney.com/api/FundGuide.aspx?dt=0&ft=gp&sd=&ed=&cp='
aimUrl_end = '&sc=z&st=desc&pi=1&pn=20&zf=diy&sh=list'

JZBL_url_start = 'https://fundmobapi.eastmoney.com/FundMApi/FundInverstPositionDetail.ashx?FCODE='
JZBL_url_end = '&deviceid=Wap&plat=Wap&product=EFund&version=2.0.0&Uid=&DATE=2017-12-31'

final_df = pd.DataFrame(columns=['股票代码', '股票名称', 'GPDM', 'GPJC', 'ISINVISBL', 'JZBL', 'TEXCH', 'ZDF','ZXJ'])
# 遍历每个基金公司
for i, rows in resultList.iterrows():
    jsonStr = requests.get(aimUrl_start + rows['id'] + aimUrl_end).text[14:]
    jsonData_1 = json.loads(jsonStr)['datas']
    chiChangList = []
    # 遍历每个基金公司下每只基金，获取该基金股票持仓的数据
    for j in jsonData_1:
        chiChangList.append(j.split(',')[:4])
        gupiaoChichang_pageCode = requests.get(JZBL_url_start + str(j.split(',')[0]) + JZBL_url_end).text
        jsonData_2 = json.loads(gupiaoChichang_pageCode)['Datas']['fundStocks']
        every_JZBL_list = pd.DataFrame(jsonData_2)
        every_JZBL_list.insert(0, '股票代码', j.split(',')[0])
        every_JZBL_list.insert(1, '股票名称', j.split(',')[1])
        every_JZBL_list.insert(2, '股票类型', j.split(',')[3])
        final_df = pd.concat((final_df, every_JZBL_list), axis=0)
        print(i, j.split(',')[0], j.split(',')[1])
    time.sleep(3)