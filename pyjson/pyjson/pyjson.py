#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Compare two similar json files.
# If some fields are missing or the value of a field is different, an error message will be displayed.
#
# Version: 1.1.1
# Copyright 2018-2020 by leeyoshinari. All Rights Reserved.

import json
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class Compare:
    def __init__(self):
        self.flag = 1  # a flag, used to determine whether two files are same.
        self.new_file = None
        self.raw_file = None

    def compare(self, new_file, raw_file, encoding):
        """
        To determine whether two files are the same.
        param:
            new_file: a new file;
            raw_file: a raw file;
            encoding: coding format, default: utf-8.
        """
        self.flag = 1  # initialize
        self.new_file = new_file  # new
        self.raw_file = raw_file  # raw
        new_json = json.load(open(self.new_file, 'r', encoding=encoding))  # read json file
        raw_json = json.load(open(self.raw_file, 'r', encoding=encoding))

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
            logging.info('There are the same between "{}" and "{}".'.format(self.new_file, self.raw_file))

    def parser_dict(self, new_dict, raw_dict):
        """
        To deal the 'dict' type.
        param:
            new_dict: the dict of the new file;
            raw_dict: the dict of the raw file.
        """
        for key, value in new_dict.items():
            if key in raw_dict.keys():
                if isinstance(value, dict):  # dict type
                    self.parser_dict(value, raw_dict[key])

                elif isinstance(value, list):  # list type
                    self.parser_list(value, raw_dict[key])

                else:
                    self.is_equal(value, raw_dict[key], key)

            else:
                self.flag = 0
                logging.error('The key "{}" is not in raw file "{}"'.format(key, self.raw_file))

    def parser_list(self, new_list, raw_list):
        """
        To deal the 'list' type.
        param:
            new_dict: the dict of the new file;
            raw_dict: the dict of the raw file.
        """
        for n in range(len(new_list)):
            if isinstance(new_list[n], dict):  # dict type
                try:
                    self.parser_dict(new_list[n], raw_list[n])
                except IndexError:
                    self.flag = 0
                    logging.error('IndexError: list index out of range.')
            else:
                self.flag = 0
                logging.error('Exist illegal field. There is no dict in list.')

    def is_equal(self, value1, value2, field):
        """
        To determine whether the two values are equal.
           Currently, all types of values in the json are int, float, str, dict, list, and null.
           If there are other types that affect the accuracy of the program, you need to increase
           the support for the corresponding type.
        param:
            value1: the value of the new file;
            value2: the value of the raw file;
            field: the key in new file.
        Description:
            1 and 1.0 are equal in Python. In order to compare the values of each field
            absolutely equal, it is converted to str.
        """
        if str(value1) != str(value2):
            self.flag = 0
            logging.error('"{}" is not equal to "{}" in "{}", new file name is "{}", raw file name '
                          'is "{}"'.format(value1, value2, field, self.new_file, self.raw_file))
