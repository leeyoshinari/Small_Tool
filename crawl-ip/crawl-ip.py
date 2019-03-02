#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : Ip_crawler.py
# @Author : leeyoshinari
# @Time   : 2019/3/2 13:13

import re
import random
import logging
import argparse
import requests
import pymysql
from scrapy.selector import Selector

user_agent = [
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36',
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
	"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64; ServiceUI 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763',
	"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
	"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class IpCrawler:
	def __init__(self, url, ip, user, pwd, database, page_num):
		self.url = url
		self.ip = ip
		self.user = user
		self.password = pwd
		self.database = database
		self.page_num = page_num

		self.timeout = 10
		self.db = None
		self.cursor = None

		self.mysqlConnect()

	def mysqlConnect(self):
		"""连接MySQL"""
		logging.info('Connecting MySQL......')
		self.db = pymysql.connect(host=self.ip, user=self.user, password=self.password, database=self.database)
		self.cursor = self.db.cursor()

		sql = """
		CREATE TABLE IF NOT EXISTS {} (
				id INT UNSIGNED AUTO_INCREMENT,
				ip VARCHAR(20) NOT NULL,
				port VARCHAR(8) NOT NULL,
				protocol VARCHAR(8) NOT NULL,
				speed FLOAT NOT NULL,
				verfy_time DATETIME,
				PRIMARY KEY (id)
				);
		""".format(self.database)
		self.cursor.execute(sql)

	def crawling(self):
		"""获取页面响应数据"""
		headers = {'Referer': 'https://www.xicidaili.com/nn/',
		           'User-Agent': user_agent[random.randint(0, len(user_agent) - 1)]}

		for i in range(self.page_num):
			logging.info('Crawling the {} page......'.format(i+1))
			url = self.url + str(i + 1)
			res = requests.get(url, headers=headers, timeout=self.timeout)
			if res.status_code == 200:
				self.parse_response(Selector(res))

	def parse_response(self, response):
		"""提取响应数据"""
		ipList = response.xpath('.//table/tr')[0]
		ip = ipList.xpath('//td[2]/text()').extract()
		port = ipList.xpath('//td[3]/text()').extract()
		protocol = ipList.xpath('//td[6]/text()').extract()
		speed = ipList.xpath('//td[7]/div/@title').extract()
		verfy_time = ipList.xpath('//td[10]/text()').extract()

		for j in range(len(ip)):
			res = re.match("^(\d+(\.\d+)?)", speed[j]).group(1)
			if float(res) < 1:
				insertData = (0, ip[j], port[j], protocol[j], float(res), '20'+verfy_time[j])
				self.insert_mysql(insertData)

	def insert_mysql(self, data):
		"""将数据插入数据库"""
		sql = "INSERT INTO {} VALUES {}".format(self.database, data)
		logging.info('Inserting {}......'.format(sql))

		if self.db and self.cursor:
			try:
				self.cursor.execute(sql)
				self.db.commit()
			except Exception as e:
				self.db.rollback()
				logging.error(e)
		else:
			self.mysqlConnect()
			self.insert_mysql(data)


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--url', type=str, default='https://www.xicidaili.com/nn/', help='西刺高匿免费ip代理')
	# parser.add_argument('--url', type=str, default='https://www.kuaidaili.com/free/inha/', help='快代理高匿免费ip代理')
	parser.add_argument('--mysqlIp', type=str, default='112.85.172.89', help='数据库ip地址')
	parser.add_argument('--mysqlUser', type=str, default='root', help='数据库用户名')
	parser.add_argument('--mysqlPassword', type=str, default='123456', help='数据库密码')
	parser.add_argument('--database', type=str, default='Ip_Agent', help='数据库名称')
	parser.add_argument('--page_num', type=int, default=10, help='需要爬取的页数')

	args = parser.parse_args()

	logging.info('Start crawl......')
	crawler = IpCrawler(args.url, args.mysqlIp, args.mysqlUser, args.mysqlPassword, args.database, args.page_num)
	crawler.crawling()
	logging.info('Crawl completed!')


if __name__ == '__main__':
	main()
