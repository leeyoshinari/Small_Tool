#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari

import datetime

def utc2local(utc_time):
    """
    UTC time to local time.
    UTC time format: 2020-02-02T02:02:02.202002Z, formatting UTC timestamp according to "%Y-%m-%dT%H:%M:%S.%fZ".
    :param utc_time: UTC time
    :return: local time
    """
    local_format = "%Y-%m-%d %H:%M:%S"
    # The format "%Y-%m-%dT%H:%M:%S.%fZ" only match 6 decimal places, if it is greater than 6 digits,
    # it needs to be divided by ".", and then converted.
    # utc_format = "%Y-%m-%dT%H:%M:%S"
    # local_time = datetime.datetime.strptime(utc_time.split('.')[0], utc_format) + datetime.timedelta(hours=8)
    utc_format = "%Y-%m-%dT%H:%M:%S.%fZ"    # The format "%Y-%m-%dT%H:%M:%S.%fZ" only match 6 decimal places
    local_time = datetime.datetime.strptime(utc_time, utc_format) + datetime.timedelta(hours=8)
    return local_time.strftime(local_format)


def local2utc(local_time):
    """
    Local time to UTC time
    :param local_time: local time
    :return: UTC time
    """
    local_format = "%Y-%m-%d %H:%M:%S"
    utc_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    utc_time = datetime.datetime.strptime(local_time, local_format) - datetime.timedelta(hours=8)
    return utc_time.strftime(utc_format)


if __name__ == '__main__':
    local_time = utc2local('2020-02-02T02:02:02.202020Z')
    utc_time = local2utc(local_time)
    print(local_time, utc_time)
