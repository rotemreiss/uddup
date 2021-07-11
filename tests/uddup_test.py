#!/usr/bin/python
# coding=utf-8
from urllib.parse import urlparse
import uddup.main as u
import pytest


def test_get_query_params_keys():
    test_url = u.get_parsed_url("https://www.example.com/?foo=1&bar=2")
    params = u.get_query_params_keys(test_url.query)
    assert params == ['foo', 'bar']


def test_is_all_params_exists():
    url_a = u.get_parsed_url("https://www.example.com/?foo=1&bar=2")
    url_b = u.get_parsed_url("https://www.example.com/?foo=1&bar=2&baz=3")

    a_in_b = u.is_all_params_exists(url_a, url_b)
    b_in_a = u.is_all_params_exists(url_b, url_a)

    pytest.assume(a_in_b is False)
    pytest.assume(b_in_a is True)


def test_has_more_params():
    src_url = u.get_parsed_url("https://www.example.com/?foo=1&bar=2")
    dst_url = u.get_parsed_url("https://www.example.com/?foo=1&bar=2&baz=3")

    src_has_more_params = u.has_more_params(src_url, dst_url)
    dst_has_more_params = u.has_more_params(dst_url, src_url)

    pytest.assume(src_has_more_params is False)
    pytest.assume(dst_has_more_params is True)


def test_uddup_main():
    expected_result = [
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
    ]

    result_urls = u.main("../demo.txt", "", True, None)
    assert result_urls == expected_result


def test_uddup_filter_path():
    expected_result = [
        "http://www.example.com/",
        "https://www.example.com/",
        "https://www.example.com/about",
        "https://www.example.com/category/hidden.html",
        "https://www.example.com/category/index.php",
        "https://www.example.com/category/watches?paramkeynoval",
        "https://www.example.com/privacy-policy",
        "https://www.example.com/utf8/is/supported/בדיקה"
    ]

    result_urls = u.main("../demo.txt", "", True, "^product")
    assert result_urls == expected_result
