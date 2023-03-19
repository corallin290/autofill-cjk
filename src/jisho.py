import re
import requests
import urllib
import webbrowser

_BASE_URL = 'https://jisho.org'

_sidebar_regex = re.compile(r'      <div class="concept_light-status">\n        (.+?)\n      <\/div>\n  <\/div>')
_jlpt_regex = re.compile(r'JLPT N(\d)')

def _search(key):
    return '{}/search/{}'.format(_BASE_URL, key)

def _word(key):
    return '{}/word/{}'.format(_BASE_URL, key)

def get_info(key):
    info = {
        'Key': '',
        'Tags': set(),
    }
    if len(key) == 0:
        return info
    key = key[0]

    page = requests.get(_word(key))
    if page.status_code < 200 or page.status_code >= 300:
        return info
    if page.text.find(key) == -1:
        return info

    info['Key'] = key
    info['Tags'].add('jp')

    tags = re.findall(_sidebar_regex, page.text)[0]
    if tags.find('Common word') != -1:
        info['Tags'].add('common-word')
    jlpt = re.findall(_jlpt_regex, tags)
    if len(jlpt) != 0:
        info['Tags'].add('n{}'.format(jlpt[0]))

    return info

def open(key):
    link = urllib.parse.quote(_search(key), safe='/:')
    webbrowser.open(link)

if __name__ == '__main__':
    test_keys = ['伝統', '直接', '早い', 'しんどい']
    for key in test_keys:
        print('{}: {},'.format(key, get_info(key)))
