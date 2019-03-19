import re
import json
import math
import hashlib
import pymysql
import requests
from urllib.parse import urlencode

headers = {
	'referer': 'https://mall.jd.com/view_search-670138-6304094-99-1-20-1.html',
	'user-agent': 'Mozilla/5.0(WindowsNT10.0;	Win64;x64)AppleWebKit/537.36(KHTML, likeGecko)Chr'
	              'ome/72.0.3626.81Safari/537.36'
}


class Bra:
	def __init__(self):
		self.db = None
		self.cursor = None
		self.md5 = []

		self.connector()

	def connector(self):
		ip = '192.168.45.166'
		self.db = pymysql.connect(host=ip, user='root', password='123456', database='cosmolady')
		self.cursor = self.db.cursor()

		sql = """
	            CREATE TABLE IF NOT EXISTS cosmolady (
	    				id VARCHAR(20) NOT NULL,
	    				productId VARCHAR(20),
	    				goodRate VARCHAR(6),
	    				color VARCHAR(12),
	    				size VARCHAR(12),
	    				userLevel VARCHAR(20),
	    				userClient VARCHAR(20),
	    				content LONGTEXT,
	    				title LONGTEXT,
	    				url VARCHAR(99),
	    				time DATETIME,
	    				PRIMARY KEY (id)
	    				);
	    		"""
		self.cursor.execute(sql)

	def get_bra_url(self, url, pageNo):
		data = {
			'callback': 'jQuery9111983',
			'sortType': '0',
			'appId': '670138',
			'pageInstanceId': '66464317',
			'searchWord': '',
			'pageNo': pageNo,
			'direction': '1',
			'instanceId': '149789800',
			'modulePrototypeId': '55555',
			'moduleTemplateId': '905542',
			'refer': 'https://mall.jd.com/view_search-670138-6304094-99-1-20-1.html',
			'_': '1552575413172'
		}

		url = url + urlencode(data)
		res = requests.get(url, headers=headers)
		pattern = re.compile("\\\\")
		if res.status_code == 200:
			return re.sub(pattern, '', res.text)

	def parser_bra_url(self, response, url):
		bra_num = int(re.compile('J_resCount">(\d+)</span>').findall(response)[0])
		page_num = math.ceil(bra_num / 20)

		for i in range(page_num):
			response = self.get_bra_url(url, i)
			pattern = re.compile('<a href="(.*?)".*?target="_blank".*?title="(.*?)">(.*?)</a>.*?<a href="(.*?).*?已有',
			                     re.S)
			res = re.findall(pattern, response)
			for r in res:
				yield r

	def get_bra_info(self, response):
		pattern = re.compile('<a href="(.*?)".*?target="_blank".*?title="(.*?)">(.*?)</a>.*?<a href="(.*?).*?已有', re.S)
		res = re.findall(pattern, response)
		for r in res:
			print(r)

	def get_comment_url(self, url, page_num=0):
		productId = re.compile('(\d+)').findall(url)[0]
		data = {
			'callback': 'fetchJSON_comment98vv156',
			'productId': productId,
			'score': 0,
			'sortType': 5,
			'page': page_num,
			'pageSize': 10,
			'isShadowSku': 0,
			'rid': 0,
			'fold': 1
		}
		comment_url = 'https://sclub.jd.com/comment/productPageComments.action?'
		url = comment_url + urlencode(data)
		res = requests.get(url, headers=headers)
		if res.status_code == 200:
			pattern = re.compile(".*?\((.*?)\);")
			res = re.findall(pattern, res.text)

			return json.loads(res[0]), productId

	def parser_comment_url(self, url, title):
		print('正在爬取 {}：{}'.format(title, url))
		if not self.duplicate(url):
			try:
				data, productId = self.get_comment_url(url)
				self.get_data(url, data, title, productId)
			except Exception as e:
				print(e)
				self.parser_comment_url(url, title)

	def get_data(self, url, data, title, productId):

		def client_re(x):
			try:
				return re.search('^来自(.*?)$', x).group(1)
			except:
				return ''

		def braSize(x):
			try:
				return re.compile('([6-9][0-9][A-G])').findall(x)[0]
			except:
				return None

		goodRate = str(data['productCommentSummary']['goodRateShow']) + "%"
		maxPage = int(data['maxPage'])
		for i in range(maxPage):
			data, _ = self.get_comment_url(url, i)
			for comments in data['comments']:
				flag = braSize(comments['productSize'])
				if not flag:
					continue

				try:
					Id = comments['discussionId']
				except:
					Id = comments['id']
				# guid = comments['guid']
				content = comments['content']
				creationTime = comments['creationTime']
				productColor = comments['productColor']
				color = productColor.split('-')[-1] if '色' in productColor else productColor.split('-')[-1] + '色'
				productSize = flag
				userLevelName = comments['userLevelName']
				# mobileVersion = comments['mobileVersion']
				userClientShow = client_re(comments['userClientShow'])

				self.insert_mysql((Id, productId, goodRate, color, productSize, userLevelName,
				                   userClientShow, content, title, url, creationTime))

	def insert_mysql(self, data):
		sql = "INSERT IGNORE INTO cosmolady VALUES {};".format(data)

		if self.db and self.cursor:
			try:
				self.cursor.execute(sql)
				self.db.commit()
			except Exception as e:
				self.db.rollback()
				print(e)
		else:
			self.connector()
			self.insert_mysql(data)

	def duplicate(self, x):
		flag = 1
		m = hashlib.md5(str(x).encode('utf-8'))

		# md5 = m.hexdigest()
		# if md5 not in self.md5:
		# 	self.md5.append(md5)
		# 	flag = 0

		if x not in self.md5:
			self.md5.append(x)
			flag = 0

		return flag


def main():
	bra = Bra()
	url = 'https://module-jshop.jd.com/module/allGoods/goods.html?'
	first_page = bra.get_bra_url(url, 1)
	for comment in bra.parser_bra_url(first_page, url):
		bra.parser_comment_url(comment[0], comment[1])


if __name__ == '__main__':
	main()
