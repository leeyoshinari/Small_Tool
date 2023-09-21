#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Compare two similar json files.
If some fields are missing or the value of a field is different, an error message will be displayed.

Version: 1.4.1
Github: https://github.com/leeyoshinari/Small_Tool/tree/master/pyjson
Copyright 2023-2025 by leeyoshinari. All Rights Reserved.
"""

import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Compare:
    def __init__(self):
        self.flag = 1  # a flag, used to determine whether two files are same.
        self.field = ['']   # a list, store the fields that traverse the dict.

    def compare(self, file1, file2, encoding):
        """
        To determine whether two files are the same.
        param:
            file1: a new file;
            file2: a raw file;
            encoding: coding format, default: utf-8.
        """
        self.flag = 1  # initialize
        new_json = json.load(open(file1, 'r', encoding=encoding))  # read json file
        raw_json = json.load(open(file2, 'r', encoding=encoding))

        # If new_json and raw_json are the 'dict' type or 'list' type, compare them,
        # otherwise throw an error.
        if isinstance(new_json, dict) and isinstance(raw_json, dict):
            self.parser_dict(new_json, raw_json)

        elif isinstance(new_json, list) and isinstance(raw_json, list):
            self.parser_list(new_json, raw_json)

        else:
            self.flag = 0
            logging.error('The file is not JSON.')

        # If flag is true, it means two files are the same.
        if self.flag:
            logging.info('There are the same between "{}" and "{}".'.format(file1, file2))

    def parser_dict(self, dict1, dict2):
        """
        To deal the 'dict' type.
        """
        if isinstance(dict2, dict):
            for key, value in dict1.items():
                self.field.append(key)
                if key in dict2.keys():
                    if isinstance(value, dict):
                        self.parser_dict(value, dict2[key])
                    elif isinstance(value, list):
                        self.parser_list(value, dict2[key])
                    else:
                        self.is_equal(value, dict2[key])
                else:
                    self.flag = 0
                    logging.error('The key "{}" is not in the second. KEY in "{}".'.format(key, self.log_str()))
                if self.field: self.field.pop()
        else:
            self.is_equal(dict1, dict2)


    def parser_list(self, list1, list2):
        """
        To deal the 'list' type.
        """
        if len(list1) == len(list2):
            if list1 and list2:
                for n in range(len(list1)):
                    self.field.append('[{}]'.format(n))
                    if isinstance(list1[n], dict):
                        self.parser_dict(list1[n], list2[n])
                    else:
                        if self.field: self.field.pop()
                        self.is_equal(list1, list2)
                        break
                    if self.field: self.field.pop()
            else:
                self.is_equal(list1, list2)
        else:
            self.flag = 0
            logging.error('The length of list is different, KEY in "{}".'.format(self.log_str()))

    def is_equal(self, value1, value2):
        """
        To determine whether the two values are equal.
        """
        if str(value1) != str(value2):
            self.flag = 0
            logging.error('"{}" is not equal to "{}" in "{}".'.format(value1, value2, self.log_str()))

    def log_str(self):
        """
        Splice the fields, used for finding the error field in dict.
        """
        res = ''
        if len(self.field) > 1:
            last = self.field[-1]
            for r in self.field[1:-1]:
                res += r + ' -> '
            return res + last
        else:
            return ''

    def sort(self, dict1: dict, reverse=False, response='dict'):
        """
            Recursively iterate and sort the keys in the dict.
        """
        res = self.sort_key(dict1, reverse)
        if response == 'dict':
            return res
        else:
            return json.dumps(res, ensure_ascii=False)

    def sort_key(self, dict1: dict, reverse=False):
        res = dict()
        keys = sorted(dict1.keys(), key=lambda x: x[0], reverse=reverse)
        for k in keys:
            if isinstance(dict1[k], dict):
                res.update({k: self.sort_key(dict1[k], reverse=reverse)})
            else:
                res.update({k: dict1[k]})
        return res
