#!/usr/bin/python
# coding=utf-8
from urllib.parse import urlparse
import uddup.main
import pytest

def test_uddup_main():
    existing_urls = uddup.main.main("./demo.txt", "", True)

    expected_result = set()
    with open("./demo-result.txt", 'r') as f:
        for url in f:
            expected_result.add(urlparse(url.rstrip()))

    assert existing_urls == expected_result
