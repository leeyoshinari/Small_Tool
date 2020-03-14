#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari

import asyncio
from aiohttp import web


async def login(request):
	# data = await request.json()   # get request data
	# name = data.get('name')       # get value by key
	# pwd = data.get('password')    # get value by key

	# with open('requestData.txt', 'w') as f:   # write request data to `.txt`
	# 	f.write(json.dumps(data))

	# return response data
	return web.json_response({'code': 0, 'message': '登陆成功', 'data': 0})


async def logout(request):
	name = request.match_info['name']   # get value by key
	return web.json_response({'code': 0, 'message': f'{name}退出成功', 'data': 0})


async def mock():
	app = web.Application()

	# add route
	app.router.add_route('POST', '/login', login)
	app.router.add_route('GET', '/logout/{name}', logout)   # get method, params can be transferred by url.

	runner = web.AppRunner(app)
	await runner.setup()
	site = web.TCPSite(runner, '127.0.0.1', 5555)   # ip and port
	await site.start()


loop = asyncio.get_event_loop()
loop.run_forever()
