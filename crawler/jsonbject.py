import json
import execjs
import requests

res = requests.get('http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=gp&rs=&gs=0&sc=zzf&st=desc&sd=2017-03-14&ed=2018-03-14&qdii=&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.4068353464561987')
res.encoding='utf-8'
# print(execjs.compile(res.text))
dict_result = execjs.eval(res.text.lstrip('var rankData = ').rstrip(';'))
print(dict_result['datas'])
# print(json.loads(str()))