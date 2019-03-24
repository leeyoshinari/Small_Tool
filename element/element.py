#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : element.py
# @Author : leeyoshinari

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import webDriverWait


class ElementExistException(Exception):
	pass


class Element(object):
	def __init__(self, driver):
		self.driver = driver
		self.timeout = 10
	
	def find_ele_by_id(self, ele):
		try:
			webDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located((By.ID, ele)))
			return self.driver.find_element_by_id(ele)
		except ElementExistException as e:
			print(e)
