import re

from . import jisho
from . import util
from . import wiktionary

def format_pinyin(pinyin_list, hanzi):
    return [py for py in pinyin_list if len(py) == len(hanzi)]

def _add_tag_to_kana(kana, tag_open, tag_close, start, end):
    old_i, old_j = start
    i, j = end
    if i >= len(kana):
        i = len(kana)-1
        j = len(kana[i])
    
    kana[i] = kana[i][:j] + tag_close + kana[i][j:]
    
    if old_i != i:
        kana[i] = tag_open + kana[i]
        for k in range(old_i+1, i):
            kana[k] = tag_open + kana[k] + tag_close
        kana[old_i] = kana[old_i] + tag_close
        
    kana[old_i] = kana[old_i][:old_j] + tag_open + kana[old_i][old_j:]
    
    return kana

def _add_pitch_single(kana, pitch):
    i = 0
    j = 0
    kana = [k for k in kana]
    for level, span in pitch:
        old_i = i
        old_j = j
        length = len(span)
        while length > 0:
            if j + length < len(kana[i]):
                j = j + length
                length = 0
            else:
                length -= len(kana[i]) - j
                i += 1
                j = 0
        
        if level == 1:
            kana = _add_tag_to_kana(kana, '<b>', '</b>', (old_i, old_j), (i, j))
        if level == 2:
            kana = _add_tag_to_kana(kana, '<span style="color: rgb(255, 38, 0);"><b>', '</b></span>', (old_i, old_j), (i, j))
            
    return kana

def _match_kana(ksimple, psimple):
    if len(ksimple) != len(psimple):
        return False
    for k,p in zip(ksimple, psimple):
        if k != p and p != 'ー':
            return False
    return True

def add_pitch(kana, pitch):
    ret = []
    i = 0
    for k in kana:
        ksimple = ''.join(k)
        if i < len(pitch) and _match_kana(ksimple,  ''.join([elt[1] for elt in pitch[i]])):
            ret.append(_add_pitch_single(k, pitch[i]))
            i += 1
        else:
            ret.append(k)
    return ret

def add_furigana(kanji, furiganas):
    if len(kanji) == 0:
        return ''
    kanji = kanji[0]
    if len(furiganas) == 0:
        return kanji

    ret = []
    for furigana in furiganas:
        if len(kanji) == len(furigana):
            with_furi = ""
            for char, furi in zip(kanji, furigana):
                with_furi += '{}[{}]'.format(char, furi)
            ret.append(with_furi)
        else:
            ret.append('{}[{}]'.format(kanji, ''.join(furigana)))
    return '\n'.join(ret)

def get_fields(key):
    key = util.normalize_unicode(key)
    info = wiktionary.get_info(key)
    # TODO: pull pitch info from OJAD if Wiktionary doesn't have it

    if info['Key'] != '':
        k = info['繁體']
        if len(k) > 0:
            k = k[0]
        else:
            k = info['新字体']
            if len(k) > 0:
                k = k[0]
            else:
                k = key
        key = k

    shinjitai = key
    if len(info['新字体']) != 0:
        shinjitai = info['新字体']
    jinfo = jisho.get_info(shinjitai)

    pinyin = format_pinyin(info['拼音'], info['Key'])
    kana = add_pitch(info['かな'], info['pitch'])
    linedict_key = ''
    if len(info['简体']) != 0:
        linedict_key = info['简体'][0]
    elif len(info['繁體']) != 0:
        linedict_key = info['繁體'][0]
    ojad_key = ''
    if len(info['pitch']) == 0:
        ojad_key = jinfo['Key']

    return {
        'Key': key,
        '繁體': add_furigana(info['繁體'], pinyin),
        '简体': add_furigana(info['简体'], pinyin),
        '拼音': '\n'.join([' '.join(p) for p in pinyin]),
        '白話字': info['白話字'],
        '粵拼': info['粵拼'],
        'linedict-key': linedict_key,
        
        '新字体': add_furigana(info['新字体'], kana),
        'かな': '\n'.join([''.join(k) for k in kana]),
        'jisho-key': jinfo['Key'],
        'ojad-key': ojad_key,

        'Tags': info['Tags'] | jinfo['Tags'],
    }

if __name__ == '__main__':
    test_keys = ['物理', '戰爭', '戰鬥', '故郷', '為']
    for key in test_keys:
        print(get_fields(key))
