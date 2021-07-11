#!/usr/bin/python
# coding=utf-8
import argparse
import os
import re
import sys
from urllib.parse import urlparse
import multiprocessing as mp
from uddup.suffixes import web, ignored

filter_path = None

# Check if we are running this on windows platform
is_windows = sys.platform.startswith('win')

# Console Colors
if is_windows:
    # Windows deserves coloring too :D
    G = '\033[92m'  # green
    Y = '\033[93m'  # yellow
    W = '\033[0m'   # white
    try:
        import win_unicode_console, colorama
        win_unicode_console.enable()
        colorama.init()
    except:
        G = Y = W = ''
else:
    G = '\033[92m'  # green
    Y = '\033[93m'  # yellow
    W = '\033[0m'   # white


def banner():
    print("""%s
  _   _ ____      _             
 | | | |  _ \  __| |_   _ _ __  
 | | | | | | |/ _` | | | | '_ \ 
 | |_| | |_| | (_| | |_| | |_) |
  \___/|____/ \__,_|\__,_| .__/ 
                         |_|    

              %s# Coded By @2RS3C
    %s""" % (Y, G, W))


def file_arg(path):
    # from os.path import exists
    if not os.path.isfile(path):
        raise ValueError  # or TypeError, or `argparse.ArgumentTypeError
    return path


def get_existing_pattern_urls(purl, uurls):
    results = []

    url_path = get_url_path(purl)
    path_parts = url_path.split('/')

    # If there is only one path, return empty list.
    if len(path_parts) == 1:
        return results

    url_pattern = '/'.join(path_parts[:-1])

    url_schema = purl.scheme
    url_hostname = purl.hostname

    for uurl in uurls:
        # Skip different hostname and schemes (they can't be a match).
        if uurl.scheme != url_schema or uurl.hostname != url_hostname:
            continue

        # @todo Can we remove the 2nd get_url_path in ddup_urls_list?
        uurl_path = get_url_path(uurl)
        if uurl_path.startswith(url_pattern):
            results.append(uurl)

    return results


def get_query_params_keys(parsed_url_query):
    keys = []
    qparams = parsed_url_query.split('&')
    for q in qparams:
        keys.append(q.split('=')[0])

    return keys


def is_all_params_exists(old_pattern, new_pattern):
    old_params_keys = get_query_params_keys(old_pattern.query)
    new_params_keys = get_query_params_keys(new_pattern.query)

    for k in new_params_keys:
        if k not in old_params_keys:
            return False

    return True


def has_more_params(old_pattern, new_pattern):
    old_params_keys = get_query_params_keys(old_pattern.query)
    new_params_keys = get_query_params_keys(new_pattern.query)
    return len(new_params_keys) > len(old_params_keys)


def get_url_path(purl):
    return purl.path.strip('/')


def get_parsed_url(url):
    url = url.rstrip()
    return urlparse(url)


def ddup_urls_list(urls_list):
    '''
    Iterate over a list of (base) URLs and dedup it.
    :param urls_list:
    :return:
    '''
    unique_urls = set()

    for parsed_url in sorted(urls_list):

        # @todo Reconsider the strip, since it can remove some interesting urls
        url_path = get_url_path(parsed_url)

        # If the URL doesn't have a path, just add it as is.
        # @todo Some dups can still occur, handle it
        if not url_path:
            unique_urls.add(parsed_url)
            continue

        # Do not add paths to common files.
        if url_path.endswith(ignored):
            continue

        # Filter paths by custom Regex if set.
        if filter_path and re.search(filter_path, url_path):
            continue

        # Add as-is paths that points to a specific web extension (e.g. html).
        if url_path.endswith(web):
            unique_urls.add(parsed_url)
            continue

        if new_pattern.path == '/product/5':
            inn = True

        # Do the more complicated ddup work.
        # Get existing URL patterns from our unique patterns.
        existing_pattern_urls = get_existing_pattern_urls(parsed_url, unique_urls)
        if not existing_pattern_urls:
            unique_urls.add(parsed_url)
        elif parsed_url.query:
            for u in existing_pattern_urls:
                # Favor URL patterns with params over those without params.
                if not u.query:
                    unique_urls.remove(u)
                    unique_urls.add(parsed_url)
                    continue

                # Check if it has query params that are extra to the unique URL pattern.
                if is_all_params_exists(u, parsed_url):
                    if has_more_params(u, parsed_url):
                        unique_urls.remove(u)
                        unique_urls.add(parsed_url)
                        continue
                else:
                    unique_urls.add(parsed_url)
                    continue

    return list(map(lambda url: url.geturl(), unique_urls))


def is_same_domain(url_a, url_b):
    '''
    Checks whether the two given urls share the same domain and scheme.
    :param url_a:
    :param url_b:
    :return: boolean
    '''
    return url_a.hostname == url_b.hostname and url_a.scheme == url_b.scheme


def split_by_base_urls(urls_list):
    # Sort the list so we will be able to split it to multi-processes per domain.
    urls_by_base_url = []
    urls_list.sort()
    prev_url = None
    cur_base_url_urls = set()
    for url in urls_list:
        parsed_url = get_parsed_url(url)

        # If the URL is in different domain (and scheme) from the previous one, split to a new list.
        if prev_url and not is_same_domain(prev_url, parsed_url):
            urls_by_base_url.append(cur_base_url_urls)
            cur_base_url_urls = set()

        cur_base_url_urls.add(parsed_url)
        prev_url = parsed_url

    # Add the last set to our list.
    urls_by_base_url.append(cur_base_url_urls)

    return urls_by_base_url


def main(urls_file, output, silent, filter_path_arg):
    global filter_path
    filter_path = filter_path_arg

    # Every tool needs a banner.
    if not silent:
        banner()

    # Iterate over the given domains
    urls_list = open(urls_file, 'r', encoding="utf-8").read().splitlines()

    urls_by_base_url = split_by_base_urls(urls_list)
    if not silent:
        print('[-] The given list contains %d unique base URLs.' % (len(urls_by_base_url)))

    # Run dedup in parallel (split by base URLs).
    # @todo allow limiting the pool size.
    # @todo Start using multiprocesses only from high amount of lines.
    processes = min(len(urls_by_base_url), mp.cpu_count())

    pool = mp.Pool(processes)
    ddup_results = pool.map(ddup_urls_list, urls_by_base_url)
    pool.close()
    pool.join()

    # "Merge" all the results to one list.
    unique_urls = list(set().union(*ddup_results))

    # Sort the results.
    unique_urls.sort()

    # @todo Print the results within the processes (although it might create high IO throughput).
    print_results(unique_urls, output)
    return unique_urls


def print_results(uurls, output):
    if output:
        try:
            f = open(output, "w")

            for url in uurls:
                f.write(url + "\n")
                print(url)

            f.close()
        except:
            print('[X] Failed to save the output to a file.')
    else:
        for url in uurls:
            print(url)


def interactive():
    parser = argparse.ArgumentParser(description='Remove URL pattern duplications..')

    # Add the arguments
    parser.add_argument('-u', '--urls', help='File with a list of urls.', type=file_arg, dest='urls_file', required=True)
    parser.add_argument('-o', '--output', help='Save results to a file.', dest='output')
    parser.add_argument('-s', '--silent', help='Print only the result URLs.', action='store_true', dest='silent')
    parser.add_argument('-fp', '--filter-path', help='Filter paths by a given Regex.', dest='filter_path')
    args = parser.parse_args()

    main(args.urls_file, args.output, args.silent, args.filter_path)


if __name__ == "__main__":
    interactive()
