#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : timeout.py
# @Author : leeyoshinari

import threading
import traceback


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
					except:
						self.error = traceback.format_exc()

			t = Timeoutlimit()
			t.setDaemon(True)
			t.start()
			t.join(timeout)

			if t.isAlive():
				raise TimeOutException('Function "{}" Running TimeOut.'.format(functions.__name__))

			if t.error:
				raise Exception(t.error)

			return t.result

		return decorator1

	return decorator


if __name__ == '__main__':
	@timeoutlimit(1)
	def sleep():
		import time
		time.sleep(2)
		return True
	print(sleep())
