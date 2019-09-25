#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari

import glob
import difflib


class FindError(object):
	def __init__(self):
		self.threshold = 0.9    # The similarity of two error messages.
		self.result = 'result.txt'  # Save error
		self.errors = []

		self.writer = open(self.result, 'w')

	def get_diff_ratio(self, str1, str2):
		"""
			Calculate similarity of `str1` and `str2`.
		"""
		ratio = difflib.SequenceMatcher(None, str1, str2).quick_ratio()
		if ratio > self.threshold:
			return True
		else:
			return False

	def write_result(self, line, log_name, error, detail):
		"""
			Write error messages to file.
		"""
		self.writer.write(f'{log_name}\tline{line}\n')
		self.writer.write(error)
		for line in detail:
			self.writer.write(line)

		self.writer.write('\n' * 5)

	def read_log(self, path):
		logs = glob.glob(path)
		for log in logs:
			print(f'Dealing {log}......')
			with open(log, 'r', encoding='utf-8') as f:
				lines = f.readlines()

			for i in range(len(lines)):
				if 'ERROR' in lines[i]:
					error = lines[i]
					error_list = []
					for j in range(i+1, len(lines)):
						if 'INFO' in lines[j] or 'ERROR' in lines[j]:
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
						self.write_result(i, log, error, error_list)

	def __del__(self):
		self.writer.close()


if __name__ == '__main__':
	log_path = './*.log'
	err = FindError()
	err.read_log(log_path)
	del err
