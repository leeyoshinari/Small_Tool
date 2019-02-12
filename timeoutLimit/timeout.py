#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : timeout.py
# @Author : leeyoshinari
# @Time   : 2019/2/12 10:24

import threading


class TimeOutException(Exception):
	pass


def timeoutlimit(timeout):
	def decorator(functions):
		def decorator1(*args, **kwargs):
			class Timeoutlimit(threading.Thread):
				def __init__(self):
					super(Timeoutlimit, self).__init__()
					self.result = None
					self.error = None
					
				def run(self):
					try:
						self.result = functions(*args, **kwargs)
					except TimeOutException as e:
						self.error = e
				
			t = Timeoutlimit()
			t.setDaemon(True)
			t.start()
			t.join(timeout)
			
			if t.error is not None:
				print('timeout:', t.error)
				
			return t.result
			
		return decorator1
	return decorator


if __name__ == '__main__':
	@timeoutlimit(1)
	def sleep():
		import time
		time.sleep(3)
		return True
	
	print(sleep())
