import re
import requests
import urllib
import webbrowser

_BASE_URL = 'https://www.gavo.t.u-tokyo.ac.jp/ojad'

def _search(key):
    return '{}//search/index/word:{}'.format(_BASE_URL, key)

def open(key):
    link = urllib.parse.quote(_search(key), safe='/:?=#')
    webbrowser.open(link)

if __name__ == '__main__':
    test_keys = ['充実', '携帯', '音楽']
    for test in test_keys:
        print(_search(test))
