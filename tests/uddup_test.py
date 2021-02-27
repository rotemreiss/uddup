#!/usr/bin/python
# coding=utf-8
from urllib.parse import urlparse
import uddup.main
import pytest

def test_uddup_main():
    expected_result_raw = (
        "http://www.example.com/",
        "https://www.example.com/",
        "https://www.example.com/about",
        "https://www.example.com/category/hidden.html",
        "https://www.example.com/category/index.php",
        "https://www.example.com/category/watches?paramkeynoval",
        "https://www.example.com/privacy-policy",
        "https://www.example.com/product/123?is_prod=false",
        "https://www.example.com/product/456?foo=bar&main=true",
        "https://www.example.com/product/456?is_debug=true&main=true&baz=2",
        "https://www.example.com/utf8/is/supported/בדיקה",
        "https://www.example2.com/product/2?is_prod=true"
    )

    expected_result = set()
    for url in expected_result_raw:
        expected_result.add(urlparse(url.rstrip()))

    existing_urls = uddup.main.main("./demo.txt", "", True, None)
    assert existing_urls == expected_result


def test_uddup_filter_path():
    expected_result_raw = (
        "http://www.example.com/",
        "https://www.example.com/",
        "https://www.example.com/about",
        "https://www.example.com/category/hidden.html",
        "https://www.example.com/category/index.php",
        "https://www.example.com/category/watches?paramkeynoval",
        "https://www.example.com/privacy-policy",
        "https://www.example.com/utf8/is/supported/בדיקה"
    )

    expected_result = set()
    for url in expected_result_raw:
        expected_result.add(urlparse(url.rstrip()))

    existing_urls = uddup.main.main("./demo.txt", "", True, "^product")
    assert existing_urls == expected_result
