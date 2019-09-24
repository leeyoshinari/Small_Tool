#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari

import glob
import difflib


class FindError(object):
	def __init__(self):
		self.threshold = 0.9
		self.result = 'result.txt'
		self.errors = []

		self.writer = open(self.result, 'w')

	def get_diff_ratio(self, str1, str2):
		ratio = difflib.SequenceMatcher(None, str1, str2).quick_ratio()
		print(ratio)
		if ratio > self.threshold:
			return True
		else:
			return False

	def write_result(self, log_name, error, detail):
		self.writer.write(log_name)
		self.writer.write(error)
		for line in detail:
			self.writer.write(line)

		for l in range(5):
			self.writer.write('\n')

	def read_log(self, path):
		logs = glob.glob(path)
		for log in logs:
			with open(log, 'r') as f:
				lines = f.readlines()

			for i in range(len(lines)):
				if 'ERROR' in lines[i]:
					error = lines[i]
					error_list = []
					for j in range(i+1, len(lines)):
						if 'INFO' in lines[j]:
							break
						error_list.append(lines[j])

					flag = 0
					if error_list:
						error_str = ''.join(error_list)
					else:
						error_str = error

					for s in self.errors:
						if self.get_diff_ratio(s, error_str):
							flag = 1
							break

					if flag == 0:
						self.errors.append(error_str)
						self.write_result(log, error, error_list)

	def __del__(self):
		self.writer.close()


if __name__ == '__main__':
	log_path = ''
	err = FindError()
	err.read_log(log_path)
	del err
