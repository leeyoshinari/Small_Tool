#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
"""
Compare two similar json files.
If some fields are missing or the value of a field is different, an error message will be displayed.

Version: 1.4.3
Github: https://github.com/leeyoshinari/Small_Tool/tree/master/pyjson
Releases: https://github.com/leeyoshinari/Small_Tool/releases
Copyright by leeyoshinari. All Rights Reserved.
"""

from pyjson.pyjson import Compare

__all__ = ["compare", "compare_dict", "compare_list", "is_equal", "flag", "sort"]

C = Compare()


def compare(file1: str, file2: str, exact_equal: bool = False, exclude_fields: list = None, encoding='utf-8'):
    """
    To determine whether two files are the same.

    param:
        file1: the path of compared file, the format is '.txt' or '.json';
        file2: the path of comparing file, the format is '.txt' or '.json';
        exact_equal: for example:
            If exact_equal = True, 2 is equal to 2.0, but '2' is not equal to 2
            If exact_equal = False, 2 is not equal to 2.0, but '2' is equal to 2
        exclude_fields: the keys that do not need to be compared; it is 'list'.
        encoding: coding format, default: utf-8.
    """
    C.compare(file1, file2, exact_equal=exact_equal, exclude_fields=exclude_fields, encoding=encoding)


def compare_dict(dict1: dict, dict2: dict, exact_equal: bool = False, exclude_fields: list = None):
    """
    To deal the 'dict' type.
    param:
        dict1: compared dict, it's a dict;
        dict2: comparing dict, it's a dict;
    """
    C.parser_dict(dict1, dict2, exact_equal=exact_equal, exclude_fields=exclude_fields)


def compare_list(list1:list, list2:list, exact_equal: bool = False, exclude_fields: list = None):
    """
    To deal the 'list' type.
    """
    C.parser_list(list1, list2, exact_equal=exact_equal, exclude_fields=exclude_fields)


def is_equal(value1, value2, exact_equal=False):
    """
    To determine whether the two values are equal.
    """
    C.is_equal(value1, value2, exact_equal=exact_equal)


def flag():
    """
    A flag that whether of two files or two values are same.
    If same, return 1, or return 0.
    """
    return C.flag


def sort(dict1: dict, reverse: bool = False, response: str = 'dict'):
    """
    Recursively iterate and sort the keys in the dict.
    param:
        response='dict' is mean to return-value is 'dict' type, it is default.
            or response='json' is mean to return-value is a json string.
    """
    return C.sort(dict1, reverse, response)
