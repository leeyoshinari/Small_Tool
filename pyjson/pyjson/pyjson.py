#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari

import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Compare:
    def __init__(self):
        self.flag = 1  # a flag, used to determine whether two files are same.
        self.field = ['']   # a list, store the fields that traverse the dict.

    def parser_file(self, benchmark_file: str, compare_file: str, exact_equal: bool, exclude_fields: list, encoding: str):
        """
        To determine whether two files are the same.
        param:
            benchmark_file: a benchmark file;
            compare_file: a compare file;
            exact_equal: for example:
                If exact_equal = True, 2 is equal to 2.0, but '2' is not equal to 2
                If exact_equal = False, 2 is not equal to 2.0, but '2' is equal to 2
            exclude_fields: the keys that do not need to be compared; it is 'list'.
            encoding: coding format, default: utf-8.
        """
        self.flag = 1  # initialize
        benchmark_json = json.load(open(benchmark_file, 'r', encoding=encoding))  # read json file
        compare_json = json.load(open(compare_file, 'r', encoding=encoding))

        # If benchmark_json and compare_json are the 'dict' type or 'list' type, compare them,
        # otherwise throw an error.
        if isinstance(benchmark_json, dict) and isinstance(compare_json, dict):
            self.parser_dict(benchmark_json, compare_json, exact_equal, exclude_fields)

        elif isinstance(benchmark_json, list) and isinstance(compare_json, list):
            self.parser_list(benchmark_json, compare_json, exact_equal, exclude_fields)

        else:
            self.flag = 0
            logging.error('The file is not JSON.')

        # If flag is true, it means two files are the same.
        if self.flag:
            logging.info('There are the same between "{}" and "{}".'.format(benchmark_file, compare_file))

    def parser_dict(self, benchmark_dict: dict, compare_dict: dict, exact_equal: bool, exclude_fields: list):
        """
        To deal the 'dict' type.
        """
        if isinstance(benchmark_dict, dict) and isinstance(compare_dict, dict):
            for key, value in benchmark_dict.items():
                if key in exclude_fields: continue
                self.field.append(key)
                if key in compare_dict.keys():
                    if isinstance(value, dict):
                        self.parser_dict(value, compare_dict[key], exact_equal, exclude_fields)
                    elif isinstance(value, list):
                        self.parser_list(value, compare_dict[key], exact_equal, exclude_fields)
                    else:
                        self.is_equal(value, compare_dict[key], exact_equal)
                else:
                    self.flag = 0
                    logging.error('The key "{}" is not in the compare file. KEY in "{}".'.format(key, self.log_str()))
                if self.field: self.field.pop()

            for key, _ in compare_dict.items():
                if key in exclude_fields: continue
                if key not in benchmark_dict.keys():
                    self.flag = 0
                    logging.error('The key "{}" is not in the benchmark file.'.format(key))
                if self.field: self.field.pop()
        else:
            self.is_equal(benchmark_dict, compare_dict, exact_equal)

    def parser_list(self, benchmark_list: list, compare_list: list, exact_equal: bool, exclude_fields: list):
        """
        To deal the 'list' type.
        """
        if len(benchmark_list) == len(compare_list):
            if benchmark_list and compare_list:
                for n in range(len(benchmark_list)):
                    self.field.append('[{}]'.format(n))
                    if isinstance(benchmark_list[n], dict):
                        self.parser_dict(benchmark_list[n], compare_list[n], exact_equal, exclude_fields)
                    else:
                        if self.field: self.field.pop()
                        self.is_equal(benchmark_list, compare_list, exact_equal)
                        break
                    if self.field: self.field.pop()
            else:
                self.is_equal(benchmark_list, compare_list, exact_equal)
        else:
            self.flag = 0
            logging.error('The length of list is different, KEY in "{}".'.format(self.log_str()))

    def is_equal(self, benchmark_value, compare_value, exact_equal: bool):
        """
        To determine whether the two values are equal.
        If exact_equal = True, 2 is equal to 2.0, but '2' is not equal to 2
        If exact_equal = False, 2 is not equal to 2.0, but '2' is equal to 2
        """
        if exact_equal:
            if benchmark_value != compare_value:
                self.flag = 0
                logging.error('"{}" is not equal to "{}" in "{}".'.format(benchmark_value, compare_value, self.log_str()))
        else:
            if str(benchmark_value) != str(compare_value):
                self.flag = 0
                logging.error('"{}" is not equal to "{}" in "{}".'.format(benchmark_value, compare_value, self.log_str()))

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

    def sort(self, sort_dict: dict, reverse: bool = False, response: str = 'dict'):
        """
            Recursively iterate and sort the keys in the dict.
        """
        res = self.sort_key(sort_dict, reverse)
        if response == 'dict':
            return res
        else:
            return json.dumps(res, ensure_ascii=False)

    def sort_key(self, sort_dict: dict, reverse: bool = False):
        res = dict()
        keys = sorted(sort_dict.keys(), key=lambda x: x[0], reverse=reverse)
        for k in keys:
            if isinstance(sort_dict[k], dict):
                res.update({k: self.sort_key(sort_dict[k], reverse=reverse)})
            else:
                res.update({k: sort_dict[k]})
        return res
