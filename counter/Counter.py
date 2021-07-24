#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari

class Counter:
    """
    统计函数执行次数
    """
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)


if __name__ == '__main__':
    @Counter
    def add(x):
        return (1+x)*x/2

    for i in range(10):
        add(i)

    print(add.count)