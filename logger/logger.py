#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: leeyoshinari

import os
import datetime
import logging.handlers


LEVEL = 'INFO'		# 日志级别可以设置到项目的配置文件里
log_path = 'logs'	# 日志路径可以设置到项目的配置文件里

"""
mode=1: 日志按文件大小切分，默认大小为10M，默认保存最近10个日志；
mode=2: 日志按时间切分，默认为按天切分，默认保存最近10个日志；
mode=3: 日志输出到控制台；
"""
mode = 3

if not os.path.exists(log_path):
	os.mkdir(log_path)

log_level = {
	'DEBUG': logging.DEBUG,
	'INFO': logging.INFO,
	'WARNING': logging.WARNING,
	'ERROR': logging.ERROR,
	'CRITICAL': logging.CRITICAL
}

logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(threadName)s:%(thread)d - %(filename)s[line:%(lineno)d] - %(message)s')
logger.setLevel(level=log_level.get(LEVEL))

if mode == 1:
	current_day = datetime.datetime.now().strftime('%Y-%m-%d')
	log_name = os.path.join(log_path, current_day + '.log')
	file_handler = logging.handlers.RotatingFileHandler(filename=log_name, maxBytes=10*1024*1024, backupCount=10)

if mode == 2:
	file_handler = logging.handlers.TimedRotatingFileHandler(os.path.join(log_path, 'logs.log'), when='midnight', interval=1, backupCount=10)
	file_handler.suffix = '%Y-%m-%d.log'

if mode == 3:
	file_handler = logging.StreamHandler()

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


if __name__ == '__main__':
	logger.info('Hello Word')
