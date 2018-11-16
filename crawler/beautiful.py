from bs4 import BeautifulSoup

html = '<!DOCTYPE html>\
	<html>\
	<head>\
		<style type="text/css">	.p_class{background:red}\
		</style>\
	<meta charset="utf-8">\
	<title>菜鸟教程(runoob.com)</title>\
	</head>\
	<body>\
	<h1>我的第一个标题</h1>\
    <a id="baidu" href="https://www.baidu.com/">这是一个指向百度的链接</a>\
	<p class="p_class">我的第一个段落。</p>\
	<p class="p_class">我的第二个段落。</p>\
	</body>\
	</html>'

soup = BeautifulSoup(html, "html.parser")
a_tag = soup.select('#baidu')[0]
print(a_tag['href'])

# print(soup.text)
