#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File   : handleException.py
# @Author : leeyoshinari

import traceback


def handle_exception(errors=(Exception, ), is_return=False, default_value=None):
	"""
	Handle exception, throw an exception, or return a value.
	:param errors: Exception type
	:param is_return: Whether to return 'default_value'. Default False, if exception, don't throw an exception, but return a value.
	:param default_value: If 'is_return' is True, return 'default_value'.
	:return: 'default_value'
	"""
	def decorator(func):
		def decorator1(*args, **kwargs):
			if is_return:
				try:
					return func(*args, **kwargs)
				except errors:
					print(traceback.format_exc())
					return default_value
			else:
				try:
					return func(*args, **kwargs)
				except errors:
					raise

		return decorator1
	return decorator


if __name__ == '__main__':
	@handle_exception(is_return=True)
	def test(a):
		return 1 / a
	print(test(0))
