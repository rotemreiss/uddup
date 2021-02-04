#!/usr/bin/python
# coding=utf-8
import argparse
import sys
import os
from urllib.parse import urlparse

# Check if we are running this on windows platform
is_windows = sys.platform.startswith('win')

# Console Colors
if is_windows:
    # Windows deserves coloring too :D
    G = '\033[92m'  # green
    Y = '\033[93m'  # yellow
    B = '\033[94m'  # blue
    R = '\033[91m'  # red
    W = '\033[0m'   # white
    try:
        import win_unicode_console, colorama
        win_unicode_console.enable()
        colorama.init()
    except:
        G = Y = B = R = W = G = Y = B = R = W = ''
else:
    G = '\033[92m'  # green
    Y = '\033[93m'  # yellow
    B = '\033[94m'  # blue
    R = '\033[91m'  # red
    W = '\033[0m'   # white


def file_arg(path):
    # from os.path import exists
    if not os.path.isfile(path):
        raise ValueError  # or TypeError, or `argparse.ArgumentTypeError
    return path


def banner():
    print("""%s                                        
 
'---'%s%s

              # Coded By Rotem Reiss - @2RS3C
    """ % (B, W, B))


def get_ignored_suffixes():
    return (
        'css',
        'js',
        'gif',
        'jpg',
        'png',
        'jpeg',
        'svg',
        'xml',
        'txt',
        'json',
        'ico',
        'webp',
        'otf',
        'ttf',
        'woff',
        'woff2',
        'eot',
        'swf',
        'zip',
        'pdf',
        'doc',
        'ppt',
        'docx',
        'xls',
        'xlsx',
        'ogg',
        'mp4',
        'mp3',
        'mov'
    )


def get_web_suffixes():
    return (
        'htm',
        'html',
        'xhtml',
        'shtml',
        'jhtml',
        'cfm',
        'jsp',
        'jspx',
        'wss',
        'action',
        'php4',
        'php5',
        'py',
        'rb',
        'pl',
        'do',
        'xml',
        'rss',
        'cgi',
        'axd',
        'asx',
        'asmx',
        'ashx',
        'asp',
        'aspx',
        'dll'
    )


def is_url_pattern_exists(pattern):
    for uurl in unique_urls:
        uurl_path = urlparse(uurl).path.strip('/')
        if uurl_path.startswith(pattern):
            return True

    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Remove URL pattern duplications..')

    # Add the arguments
    parser.add_argument('-u', '--urls', help='File with a list of urls.', type=file_arg, dest='urls_file')
    args = parser.parse_args()

    # Print our banner
    banner()

    unique_urls = set()
    web_suffixes = get_web_suffixes()
    ignored_suffixes = get_ignored_suffixes()
    # Iterate over the given domains
    with open(args.urls_file, 'r') as f:
        for url in f:
            url = url.rstrip()
            if not url:
                continue

            parsed_url = urlparse(url)

            # @todo Reconsider the rstrip, since it can remove some interesting urls
            url_path = parsed_url.path.strip('/')

            # If the URL doesn't have a path, just add it as is
            # @todo Some dups can still occur, handle it
            if not url_path:
                unique_urls.add(url)
                continue

            # Do not add paths to common files
            if url_path.endswith(ignored_suffixes):
                continue

            # Add as-is paths that points to a specific web extension (e.g. html)
            if url_path.endswith(web_suffixes):
                unique_urls.add(url)
                continue

            # Do the more complicated ddup work
            path_parts = url_path.split('/')
            if len(path_parts) == 1:
                unique_urls.add(url)
                continue

            url_pattern = '/'.join(path_parts[:-1])
            if not is_url_pattern_exists(url_pattern):
                unique_urls.add(url)

    for url in unique_urls:
        print (url)