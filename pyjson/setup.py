#!/usr/bin/env python
# -*- coding:utf-8 -*-

# File Name: setup.py
# Author: leeyoshinari


from setuptools import setup, find_packages

setup(
    name="pyjson",
    version="1.1.1",
    author="leeyoshinari",
    author_email="leeyoshinari@outlook.com",
    keywords=("pip", "pyjson", "logging"),
    description="Compare the similarities between two JSONs.",
    long_description="",
    url="https://github.com/leeyoshinari/jsontool",
    packages=find_packages(),
    install_requires=[],
    classifiers=(
            "License :: OSI Approved :: MIT License",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7"
        ),
)
