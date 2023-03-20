import re
import requests
import urllib
import webbrowser

_BASE_URL = 'https://dict.naver.com/linedict/zhendict/dict.html#/cnen'

def _search(key):
    return '{}/search?query={}'.format(_BASE_URL, key)

# TODO: this only opens up the search page and not the entry
# Is there a way to open up the entry directly?
def open(key):
    link = urllib.parse.quote(_search(key), safe='/:?=#')
    webbrowser.open(link)

if __name__ == '__main__':
    test_keys = ['传统', '沙发', '月亮']
    for test in test_keys:
        print(_search(test))
