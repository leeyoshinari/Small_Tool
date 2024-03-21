#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
"""
Compare two similar json files.
If some fields are missing or the value of a field is different, an error message will be displayed.

Version: 1.4.6
Github: https://github.com/leeyoshinari/Small_Tool/tree/master/pyjson
Releases: https://github.com/leeyoshinari/Small_Tool/releases
Copyright by leeyoshinari. All Rights Reserved.
"""

from pyjson.pyjson import Compare

__all__ = ["compare", "flag", "sort"]

C = Compare()


def compare(benchmark_file: any, compare_file: any, compare_type: str = 'file', exact_equal: bool = False,
            exclude_fields: list = None, encoding: str = 'utf-8'):
    """
    To determine whether two files are the same.

    param:
        benchmark_file: the path of benchmark file, the format is '.txt' or '.json', dict, list;
        compare_file: the path of compare file, the format is '.txt' or '.json', dict, list;
        compare_type: file, dict or list;
            If compare_type = 'file', benchmark_file and compare_file are a json file, the format is '.txt' or '.json'.
            If compare_type = 'dict', benchmark_file and compare_file are a dict.
            If compare_type = 'list', benchmark_file and compare_file are a list.
        exact_equal: for example:
            If exact_equal = True, 2 is equal to 2.0, but '2' is not equal to 2
            If exact_equal = False, 2 is not equal to 2.0, but '2' is equal to 2
        exclude_fields: the keys that do not need to be compared; it is 'list'.
        encoding: coding format, default: utf-8.
    """
    if exclude_fields is None: exclude_fields = list()
    if compare_type == 'file':
        C.parser_file(benchmark_file, compare_file, exact_equal=exact_equal, exclude_fields=exclude_fields, encoding=encoding)

    if compare_type == 'dict':
        C.parser_dict(benchmark_file, compare_file, exact_equal=exact_equal, exclude_fields=exclude_fields)

    if compare_type == 'list':
        C.parser_list(benchmark_file, compare_file, exact_equal=exact_equal, exclude_fields=exclude_fields)


def flag():
    """
    A flag that whether of two files or two values are same.
    If same, return 1, or return 0.
    """
    return C.flag


def sort(sort_dict: dict, reverse: bool = False, response: str = 'dict'):
    """
    Recursively iterate and sort the keys in the dict.
    param:
        response='dict' is mean to return-value is 'dict' type, it is default.
            or response='json' is mean to return-value is a json string.
    """
    return C.sort(sort_dict, reverse, response)
