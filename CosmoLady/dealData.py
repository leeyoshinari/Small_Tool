# -*- coding: utf-8 -*-

import os
import re
import jieba
import pkuseg
import colorsys
import pymysql
import numpy as np
from wordcloud import WordCloud
from matplotlib import pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']


def ReadDataFromMySQL(ip, username, pwd, db):
	db = pymysql.connect(host=ip, user=username, password=pwd, database=db)
	cursor = db.cursor()

	function_cups = lambda x: re.compile('([6-9][0-9][A-G])').findall(x)[0]
	comment_id = []
	colors = []
	cups = []
	levels = []
	clients = []
	praises = []
	times = []

	sql = "SELECT id, color, size, userLevel, userClient, content, time FROM cosmolady;"
	cursor.execute(sql)
	res = cursor.fetchall()
	if res:
		for i in range(len(res)):
			if res[i][2]:
				comment_id.append(res[i][0])
				colors.append(res[i][1].split('2')[0])
				cups.append(function_cups(res[i][2]))
				levels.append(res[i][3])
				clients.append(res[i][4] if res[i][4] else '其他')
				praises.append(res[i][5])
				times.append(res[i][6])
	else:
		ReadDataFromMySQL(ip, username, pwd, db)

	return comment_id, colors, cups, praises, times, levels, clients


def parse_cup(cup):
	busts = []
	cups = []
	function_bust = lambda x: re.compile('([6-9][0-9])').findall(x)[0]
	function_cup = lambda x: re.compile('([A-G])').findall(x)[0]

	for c in cup:
		busts.append(function_bust(c))
		cups.append(function_cup(c))

	return busts, cups


def male2female(praises):
	num = 0
	female = 0
	for praise in praises:
		if '老婆' in praise or '媳妇' in praise or '女朋友' in praise or '女票' in praise:
			num += 1

		if '老公' in praise or '男朋友' in praise or '男票' in praise:
			female += 1

	return num, female


def normalize_color(colors):
	color = {'black': 0,  # 黑色
	         'grey': 0,  # 灰色
	         'white': 0,  # 白色
	         'red': 0,  # 红色
	         'pink': 0,  # 粉色
	         'blue': 0,  # 蓝色
	         'purple': 0,  # 紫色
	         'yellow': 0,  # 黄色
	         'skin': 0,  # 肤色
	         'green': 0,  # 绿色
	         'other': 0}

	for c in colors:
		if '黑' in c:
			color['black'] += 1
			continue
		elif '灰' in c:
			color['grey'] += 1
			continue
		elif '白' in c:
			color['white'] += 1
			continue
		elif '红' in c:
			color['red'] += 1
			continue
		elif '粉' in c:
			color['pink'] += 1
			continue
		elif '蓝' in c:
			color['blue'] += 1
			continue
		elif '紫' in c:
			color['purple'] += 1
			continue
		elif '黄' in c:
			color['yellow'] += 1
			continue
		elif '肤' in c:
			color['skin'] += 1
			continue
		elif '绿' in c:
			color['green'] += 1
			continue
		else:
			color['other'] += 1

	plt.figure('合并后颜色图', figsize=[9.6, 7.2])
	labels = ['黑色', '灰色', '白色', '红色', '绿色', '蓝色', '紫色', '黄色', '肤色', '粉色', '其他颜色']
	values = [color['black'], color['grey'], color['white'], color['red'], color['green'],
	          color['blue'], color['purple'], color['yellow'], color['skin'], color['pink'], color['other']]
	color_ = ['orange', 'gray', 'whitesmoke', 'red', 'lightgreen', 'skyblue', 'purple',
	          'yellow', 'wheat', 'pink', 'turquoise']
	explode = (0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02)
	plt.pie(values, explode=explode, labels=labels, colors=color_, autopct='%.2f%%', shadow=False)
	plt.axis('equal')
	plt.savefig('合并后颜色分布图.png')
	plt.show()

	return color


def count_num(mylist, items=None):
	res = {}
	if not items:
		items = set(mylist)
	for item in items:
		res.update({str(item): mylist.count(item)})

	return res


def list2_of_per_list1(list1, list2, items1=None, items2=None):
	res = {}
	if not items1:
		items1 = set(list1)
	for item in items1:
		listed = [list2[i] for i in range(len(list1)) if list1[i] == item]
		res.update({str(item): count_num(listed, items2)})

	return res


def sales(times):
	month = []
	for t in times:
		month.append(str(t)[:7])

	return count_num(month, sorted(set(month)))


def day_sales(times):
	comment = []
	for t in times:
		t = str(t)
		if '2018-11' in t:# or '2018-12' in t:
			comment.append(t.split(' ')[0])

	return count_num(comment, sorted(set(comment)))


def word_frequency(praises):
	text = [" ".join(jieba.cut(praise, cut_all=False)) for praise in praises]

	word_cloud = WordCloud(width=1920, height=1080, font_path='simhei.ttf',
	                       background_color='white').generate(' '.join(text))

	plt.figure('词云图')
	plt.imshow(word_cloud)
	plt.axis('off')
	plt.show()
	plt.imsave('word_cloud.png', word_cloud)


def plot_bar(x_label, y_label, value, title):
	def optimize_bar(rect):
		for r in rect:
			height = r.get_height()
			plt.text(r.get_x() + r.get_width() / 2, height, height, ha='center', va='bottom')
			r.set_edgecolor('white')

	color = ['red', 'orange', 'blue', 'purple', 'darkgreen']
	np.random.shuffle(color)
	plt.figure(title, figsize=[19.2, 10.8])
	index = np.arange(0.2, 10, 2.3)
	barwith = 0.4

	for i in range(len(x_label)):
		rects = plt.bar(index + i*barwith, value[i], barwith, color=color[i], label=y_label[i])
		optimize_bar(rects)

	plt.xticks(index + 2*barwith, x_label)
	plt.legend()
	plt.xlim((0, 11.6))
	plt.ylabel('数量')
	if '胸围下' in title:
		plt.xlabel('胸围')
	if '罩杯下' in title:
		plt.xlabel('罩杯')
	plt.savefig(title + '.png')
	plt.show()


def random_color(N, bright=True):
	brightness = 1.0 if bright else 0.7
	hsv = [(i / N, 1, brightness) for i in range(N)]
	colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
	np.random.shuffle(colors)
	return colors


def main():
	# ip = '192.168.31.223'
	ip = '192.168.43.160'
	username = 'root'
	pwd = '123456'
	db = 'cosmolady'

	_bust = ['70', '75', '80', '85', '90']
	_cup = ['A', 'B', 'C', 'D', 'E']
	comment_id, colors, cups, praises, times, levels, clients = ReadDataFromMySQL(ip, username, pwd, db)

	color_res = count_num(colors)
	color_label = []
	color_value = []
	for key, value in color_res.items():
		color_label.append(key)
		color_value.append(value)
	plt.figure('原始颜色图', figsize=[19.2, 10.8])
	index = np.arange(len(color_value)) * 0.5 + 0.2
	plt.bar(index, color_value, 0.4, color=random_color(len(color_value)))
	plt.xlim((0, index[-1]+0.6))
	plt.xlabel('颜色')
	plt.ylabel('数量')
	plt.xticks(index, color_label, rotation=45)
	plt.savefig('原始颜色分布图.png')
	plt.show()
	_ = normalize_color(colors)  # 对颜色进行合并
	bust, cup = parse_cup(cups)     # 获取胸围和罩杯
	cups_counter = count_num(cups)
	bust_counter = count_num(bust, _bust)  # 统计每个胸围的数量
	cup_counter = count_num(cup, _cup)    # 统计每个罩杯的数量
	cup_of_bust = list2_of_per_list1(bust, cup, _bust, _cup)     # 统计每个胸围下的罩杯的数量
	bust_of_cup = list2_of_per_list1(cup, bust, _cup, _bust)     # 统计每个罩杯下的胸围的数量
	# word_frequency(praises)
	month_sales = sales(times)
	good_male, female = male2female(praises)      # 好男人数
	print(good_male, good_male/len(colors))
	print(female, female/len(colors))

	cups_label = []
	cups_value = []
	for key, value in cups_counter.items():
		cups_label.append(key)
		cups_value.append(value)

	bust_label = []
	bust_value = []
	for key, value in bust_counter.items():
		bust_label.append(key)
		bust_value.append(value)

	cup_label = []
	cup_value = []
	for key, value in cup_counter.items():
		cup_label.append(key)
		cup_value.append(value)

	explode = (0.02, 0.02, 0.02, 0.02, 0.02)
	plt.figure('胸围图', figsize=[9.6, 7.2])
	plt.pie(bust_value, labels=bust_label, colors=random_color(5), autopct='%.2f%%', shadow=True, explode=explode)
	plt.axis('equal')
	plt.savefig('胸围分布图.png')
	plt.show()

	plt.figure('罩杯图', figsize=[9.6, 7.2])
	plt.pie(cup_value, labels=cup_label, colors=random_color(5), autopct='%.2f%%', shadow=True, explode=explode)
	plt.axis('equal')
	plt.savefig('罩杯分布图.png')
	plt.show()

	cup_num = []
	for key, value in cup_of_bust.items():
		xy_value = []
		for k, v in value.items():
			xy_value.append(v)

		cup_num.append(tuple(xy_value))

	bust_num = []
	for key, value in bust_of_cup.items():
		xy_value = []
		for k, v in value.items():
			xy_value.append(v)

		bust_num.append(tuple(xy_value))

	plot_bar(_cup, _bust, tuple(cup_num), '每个罩杯下每个胸围的数量')
	plot_bar(_bust, _cup, tuple(bust_num), '每个胸围下每个罩杯的数量')

	x_sale = []
	y_sale = []
	for key, value in month_sales.items():
		x_sale.append(key)
		y_sale.append(value)

	index = np.arange(len(x_sale))
	plt.figure('每月评价数', figsize=[19.2, 10.8])
	plt.plot(index, y_sale, color='red', marker='^', markersize=6)
	plt.xticks(index, x_sale, rotation=45)
	for x, y in zip(index, y_sale):
		plt.text(x, y, y, ha='center', va='bottom')
	plt.ylim((0, 3500))
	plt.xlabel('时间')
	plt.ylabel('评论数')
	plt.savefig('每月评论数.png')
	plt.show()

	x_sale = []
	y_sale = []
	day_sale = day_sales(times)
	for key, value in day_sale.items():
		x_sale.append(key)
		y_sale.append(value)

	index = np.arange(len(x_sale))
	plt.figure('2018年11-12月每日评价数', figsize=[19.2, 10.8])
	plt.plot(index, y_sale, color='red', marker='^', markersize=6)
	plt.xticks(index, x_sale, rotation=60)
	for x, y in zip(index, y_sale):
		plt.text(x, y, y, ha='center', va='bottom')
	plt.ylim((40, 310))
	plt.xlabel('时间')
	plt.ylabel('评论数')
	plt.savefig('2018年11-12月每日评论数.png')
	plt.show()

	userlevel = count_num(levels)
	userclient = count_num(clients)

	level_label = []
	level_value = []
	for key, value in userlevel.items():
		level_label.append(key)
		level_value.append(value)

	client_label = []
	client_value = []
	for key, value in userclient.items():
		client_label.append(key)
		client_value.append(value)

	explode = (0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02)
	plt.figure('会员图', figsize=[9.6, 7.2])
	plt.pie(level_value, labels=level_label, colors=random_color(len(userlevel)), autopct='%.2f%%', shadow=True, explode=explode)
	plt.axis('equal')
	plt.savefig('会员分布图.png')
	plt.show()
	explode = (0.02, 0.02, 0.02, 0.02, 0.02, 0.02)
	plt.figure('客户端图', figsize=[9.6, 7.2])
	plt.pie(client_value, labels=client_label, colors=random_color(len(userclient)), autopct='%.2f%%', shadow=True, explode=explode)
	plt.axis('equal')
	plt.savefig('客户端分布图.png')
	plt.show()

	print(len(colors))


if __name__ == '__main__':
	main()
