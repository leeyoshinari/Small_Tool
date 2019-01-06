#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Compare two similar json files.
# If some fields are missing or the value of a field is different, an error message will be displayed.

from pyjson.pyjson import Compare

__all__ = ["compare", "parser_dict", "parser_list", "is_equal"]

C = Compare()

def compare(new_file, raw_file, encoding='utf-8'):
    """
    To determine whether two files are the same.

    param:
        new_file: a new file;
        raw_file: a raw file;
        encoding: coding format, default: utf-8.
    """
    C.compare(new_file, raw_file, encoding=encoding)

def parser_dict(new_dict, raw_dict):
    """
    To deal the 'dict' type.

    param:
        new_dict: the dict of the new file;
        raw_dict: the dict of the raw file.
    """
    C.parser_dict(new_dict, raw_dict)

def parser_list(new_list, raw_list):
    """
    To deal the 'list' type.

    param:
        new_dict: the dict of the new file;
        raw_dict: the dict of the raw file.
    """
    C.parser_list(new_list, raw_list)

def is_equal(value1, value2, field):
    """
    To determine whether the two values are equal.
    Currently, all types of values in the json are int, float, str, dict, list, and null.
    If there are other types that affect the accuracy of the program, you need to increase
    the support for the corresponding type.

    param:
        value1: the value of the new file;
        value2: the value of the raw file;
        field: the key in new file.
    """
    C.is_equal(value1, value2, field)
