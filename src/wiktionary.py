import re
import requests
import urllib
import webbrowser

from .util import *
from . import pinyin

WIKI_BASE_URL = 'https://en.wiktionary.org'

def _passthrough(matches):
    return ''.join([remove_html_tags(normalize_unicode(m)) for m in matches])
def _process_pinyin(matches):
    return [res for m in matches for res in pinyin.split(remove_html_tags(normalize_unicode(m)))]
def _process_poj(matches):
    return ' / '.join([remove_html_tags(normalize_unicode(m)) for m in matches])
def _process_jyutping(matches):
    return ' / '.join([remove_html_tags(normalize_unicode(m)) for m in matches])
def _process_kana(matches):
    return [remove_html_tags(normalize_unicode(m)) for m in matches]

_PITCH = {
    re.compile(r'<span [^>]+>([^<&#]+?)<span [^>]+>&#8203;<\/span[^>]*?><\/span[^>]*?>'): 2,
    # TODO: none of your offline test cases had this
    re.compile(r'<span [^>]+>&#8203;<\/span[^>]*?><span [^>]+>([^<&#]+?)<\/span[^>]*?>'): 2,
    re.compile(r'<span [^>]+>([^<&#]+?)<\/span[^>]*?>'): 1,
    # TODO: can you specify kana here?
    re.compile(r'([^<&#;]*)'): 0,
}
def _process_pitch_single(pitch):
    ret = []
    while len(pitch) > 0:
        found = False
        for p in _PITCH:
            match = re.match(p, pitch)
            if match != None:
                ret.append((_PITCH[p], match.group(1)))
                pitch = pitch[match.span()[1]:]
                found = True
                break
        if not found:
            return None
    return ret

def _process_pitch(pitches):
    return [_process_pitch_single(normalize_unicode(p)) for p in pitches]

_cn_header_regex = r'<h2><span class="mw-headline" id="Chinese">Chinese<\/span><span class="mw-editsection"><span class="mw-editsection-bracket">\[<\/span><a href="\/w\/index\.php\?title=(?:.+?)&amp;action=edit&amp;section=\w+?" title="Edit section: Chinese">edit<\/a><span class="mw-editsection-bracket">]<\/span><\/span><\/h2>'

_cn_fields = {
    '繁體': (re.compile(r'<title>(.+?) - Wiktionary<\/title>'),
        _passthrough),
    '简体': (re.compile(r'<th style="padding: 0\.5em;border: 1px solid #aaa;background: #E0FFFF;font-weight: normal;font-size: smaller;" colspan="2"><a href="\/wiki\/Simplified_Chinese" title="Simplified Chinese">simp\.<\/a>(?: and <a href="\/wiki\/Traditional_Chinese" title="Traditional Chinese">trad\.<\/a>)?(?:<br \/>)? ?<span style="font-size:140%">\(<span lang="zh-Han[si]" class="Han[si]">(.+?)<\/span>\)'),
        _passthrough),
    '拼音': (re.compile(r'<dl><dd><small>\(<i><a href="https:\/\/en\.wikipedia\.org\/wiki\/Pinyin" class="extiw" title="w:Pinyin">Pinyin<\/a><\/i>\)<\/small>: <span class="form-of pinyin-\w+?-form-of(?: transliteration-[^"]+?)?" lang="cmn" style="font-family: Consolas, monospace;"><a href="\/wiki\/[^"]+?" title="[^"]+?">(.+?)<\/a>'),
        _process_pinyin),
    '白話字': (re.compile(r'<li><a href="https:\/\/en\.wikipedia\.org\/wiki\/Min_Nan" class="extiw" title="w:Min Nan">Min Nan<\/a> <small>\(<i><a href="https:\/\/en\.wikipedia\.org\/wiki\/Pe%CC%8Dh-%C5%8De-j%C4%AB" class="extiw" title="w:Pe̍h-ōe-jī">POJ<\/a><\/i>\)<\/small>: <span style="font-family: Consolas, monospace;">(.+?)<\/span>'),
        _process_poj),
    '粵拼': (re.compile(r'<li><a href="https:\/\/en\.wikipedia\.org\/wiki\/Cantonese" class="extiw" title="w:Cantonese">Cantonese<\/a> <small>\(<i><a href="https:\/\/en\.wikipedia\.org\/wiki\/Jyutping" class="extiw" title="w:Jyutping">Jyutping<\/a><\/i>\)<\/small>: <span style="font-family: Consolas, monospace;">(.+?)<\/span>'),
        _process_jyutping)
}

_jp_header_regex = r'<h2><span class="mw-headline" id="Japanese">Japanese<\/span><span class="mw-editsection"><span class="mw-editsection-bracket">\[<\/span><a href="\/w\/index\.php\?title=(?:.+?)&amp;action=edit&amp;section=\w+?" title="Edit section: Japanese">edit<\/a><span class="mw-editsection-bracket">]<\/span><\/span><\/h2>'
_shinjitai_link_regex = r'<ol><li><span class="form-of-definition use-with-mention"><a href="\/wiki\/ky%C5%ABjitai" title="kyūjitai">K(?:yūjitai)?<\/a> form of <span class="form-of-definition-link"><i class="Jpan mention" lang="ja"><a href="(.+?)#Japanese"'
_see_also_regex = r'<div id="mw-content-text" class="mw-body-content mw-content-ltr" lang="en" dir="ltr"><div class="mw-parser-output"><div class="disambig-see-also"><i>See also:<\/i>(.+?)<\/div>'
_see_also_link_regex = r'<b class="Hani"><a href="(.+?)" (?:class="new" )?title=".+?">.+?<\/a><\/b>'

_jp_fields = {
    '新字体': (re.compile(r'<title>(.+?) - Wiktionary<\/title>'),
        _passthrough),
    'かな': ((re.compile(r'<tr lang="ja" class="Jpan" style="font-size: 2em; background: white; line-height: 1em;">(?:\n<td style="padding: 0\.5em;"><a (?:class="mw-selflink-fragment" )?href="(?:\/wiki\/.+?)?#Japanese"(?: title=".+?")?>.+?<\/a>\n<\/td>)+<\/tr>\n<tr style="background: white;">(?:\n<td(?: colspan="\d+")?><span class="Jpan" lang="ja">.+?<\/span>(?:<br \/><small><a href="\/wiki\/Appendix:Japanese_glossary#.+?_kanji" title="Appendix:Japanese glossary">Grade: .<\/a><\/small>)?\n<\/td>)+<\/tr>'),
            re.compile(r'<td(?: colspan="\d+")?><span class="Jpan" lang="ja">(.+?)<\/span')),
        _process_kana),
    'pitch': (re.compile(r'<ul><li><span class="ib-brac qualifier-brac">\(<\/span><span class="ib-content qualifier-content"><a href="https:\/\/en\.wikipedia\.org\/wiki\/Tokyo_dialect" class="extiw" title="w:Tokyo dialect">Tokyo<\/a><\/span><span class="ib-brac qualifier-brac">\)<\/span> <span lang="ja" class="Jpan">(.+?)<\/span> ?<span'),
        _process_pitch)
}

def _get_jp_page(page, see_also=True):
    # If the page says it's the kyuujitai form, then follow the link to the shinjitai form
    matches = re.findall(_shinjitai_link_regex, page.text)
    if len(matches) != 0:
        return requests.get('{}/{}'.format(WIKI_BASE_URL, matches[0]))
    # Else, check whether there's a "Japanese" header. If there is, we're probably good.
    matches = re.findall(_jp_header_regex, page.text)
    if len(matches) != 0:
        return page
    
    # see_also = False, so don't check the "See also" pages
    if not see_also:
        return None
    
    see_also = re.findall(_see_also_regex, page.text)
    if len(see_also) == 0:
        # Case: no "See also" pages, so there's likely no Japanese equivalent
        return None
    matches = re.findall(_see_also_link_regex, see_also[0])
    for link in matches:
        # Check whether it gives us a kyuujitai form or a "Japanese" header
        page = requests.get('{}/{}'.format(WIKI_BASE_URL, link))
        jp_page = _get_jp_page(page, see_also=False)
        if jp_page != None:
            return jp_page
    
    return None   

def get_info(key):
    info = {'Key': key}
    page = requests.get('{}/wiki/{}'.format(WIKI_BASE_URL, key))
    # TODO: error handling
    
    matches = re.findall(_cn_header_regex, page.text)
    if len(matches) == 0:
        for field in _cn_fields:
            info[field] = ''
    else:
        for field in _cn_fields:
            regex, process_func = _cn_fields[field]
            matches = re.findall(regex, page.text)
            info[field] = process_func(matches)

    page = _get_jp_page(page)
    if page == None:
        for field in _jp_fields:
            info[field] = ''
    else:
        for field in _jp_fields:
            if field == 'かな':
                regexes, process_func = _jp_fields[field]
                regex1, regex2 = regexes
                all_readings = []
                for match in re.findall(regex1, page.text):
                    matches = re.findall(regex2, match)
                    all_readings.append(process_func(matches))
                info[field] = all_readings
            else:
                regex, process_func = _jp_fields[field]
                matches = re.findall(regex, page.text)
                info[field] = process_func(matches)

    return info

def open(key):
    link = urllib.parse.quote('{}/wiki/{}'.format(WIKI_BASE_URL, key), safe='/:')
    webbrowser.open(link)
    
if __name__ == '__main__':
    test_keys = ['物理', '戰爭', '戰鬥', '故郷', '為']
    for key in test_keys:
        print(get_info(key))