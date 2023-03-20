_pinyin_syllables = [
    'a', 'o', 'e', 'er', 'ai', 'ao', 'ou', 'an', 'en', 'ang', 'eng', 'yi', 'ya', 'yao', 'ye', 'you', 'yan', 'yin', 'yang', 'ying', 'yong', 'wu', 'wa', 'wo', 'wai', 'wei', 'wan', 'wen', 'wang', 'weng', 'yu', 'yue', 'yuan', 'yun', 
    'ba', 'bo', 'bai', 'bei', 'bao', 'ban', 'ben', 'bang', 'beng', 'bi', 'biao', 'bie', 'bian', 'bin', 'bing', 'bu', 
    'pa', 'po', 'pai', 'pei', 'pao', 'pou', 'pan', 'pen', 'pang', 'peng', 'pi', 'piao', 'pie', 'pian', 'pin', 'ping', 'pu', 
    'ma', 'mo', 'me', 'mai', 'mei', 'mao', 'mou', 'man', 'men', 'mang', 'meng', 'mi', 'miao', 'mie', 'miu', 'mian', 'min', 'ming', 'mu', 
    'fa', 'fo', 'fei', 'fou', 'fan', 'fen', 'fang', 'feng', 'fu', 
    'da', 'de', 'dai', 'dei', 'dao', 'dou', 'dan', 'den', 'dang', 'deng', 'dong', 'di', 'diao', 'die', 'diu', 'dian', 'ding', 'du', 'duo', 'dui', 'duan', 'dun', 
    'ta', 'te', 'tai', 'tei', 'tao', 'tou', 'tan', 'tang', 'teng', 'tong', 'ti', 'tiao', 'tie', 'tian', 'ting', 'tu', 'tuo', 'tui', 'tuan', 'tun', 
    'na', 'ne', 'nai', 'nei', 'nao', 'nou', 'nan', 'nen', 'nang', 'neng', 'nong', 'ni', 'niao', 'nie', 'niu', 'nian', 'nin', 'niang', 'ning', 'nu', 'nuo', 'nuan', 'nv', 'nve', 
    'la', 'le', 'lai', 'lei', 'lao', 'lou', 'lan', 'lang', 'leng', 'long', 'li', 'lia', 'liao', 'lie', 'liu', 'lian', 'lin', 'liang', 'ling', 'lu', 'luo', 'luan', 'lun', 'lv', 'lve', 
    'ga', 'ge', 'gai', 'gei', 'gao', 'gou', 'gan', 'gen', 'gang', 'geng', 'gong', 'gu', 'gua', 'guo', 'guai', 'gui', 'guan', 'gun', 'guang', 
    'ka', 'ke', 'kai', 'kei', 'kao', 'kou', 'kan', 'ken', 'kang', 'keng', 'kong', 'ku', 'kua', 'kuo', 'kuai', 'kui', 'kuan', 'kun', 'kuang', 
    'ha', 'he', 'hai', 'hei', 'hao', 'hou', 'han', 'hen', 'hang', 'heng', 'hong', 'hu', 'hua', 'huo', 'huai', 'hui', 'huan', 'hun', 'huang', 
    'za', 'ze', 'zi', 'zai', 'zei', 'zao', 'zou', 'zan', 'zen', 'zang', 'zeng', 'zong', 'zu', 'zuo', 'zui', 'zuan', 'zun', 
    'ca', 'ce', 'ci', 'cai', 'cao', 'cou', 'can', 'cen', 'cang', 'ceng', 'cong', 'cu', 'cuo', 'cui', 'cuan', 'cun', 
    'sa', 'se', 'si', 'sai', 'sao', 'sou', 'san', 'sen', 'sang', 'seng', 'song', 'su', 'suo', 'sui', 'suan', 'sun', 
    'zha', 'zhe', 'zhi', 'zhai', 'zhei', 'zhao', 'zhou', 'zhan', 'zhen', 'zhang', 'zheng', 'zhong', 'zhu', 'zhua', 'zhuo', 'zhuai', 'zhui', 'zhuan', 'zhun', 'zhuang', 
    'cha', 'che', 'chi', 'chai', 'chao', 'chou', 'chan', 'chen', 'chang', 'cheng', 'chong', 'chu', 'chua', 'chuo', 'chuai', 'chui', 'chuan', 'chun', 'chuang', 
    'sha', 'she', 'shi', 'shai', 'shei', 'shao', 'shou', 'shan', 'shen', 'shang', 'sheng', 'shu', 'shua', 'shuo', 'shuai', 'shui', 'shuan', 'shun', 'shuang', 
    're', 'ri', 'rao', 'rou', 'ran', 'ren', 'rang', 'reng', 'rong', 'ru', 'rua', 'ruo', 'rui', 'ruan', 'run', 
    'ji', 'jia', 'jiao', 'jie', 'jiu', 'jian', 'jin', 'jiang', 'jing', 'jiong', 'ju', 'jue', 'juan', 'jun', 
    'qi', 'qia', 'qiao', 'qie', 'qiu', 'qian', 'qin', 'qiang', 'qing', 'qiong', 'qu', 'que', 'quan', 'qun', 
    'xi', 'xia', 'xiao', 'xie', 'xiu', 'xian', 'xin', 'xiang', 'xing', 'xiong', 'xu', 'xue', 'xuan', 'xun'
]
_diacritic_table = {'\u0304': 1, '\u0301': 2, '\u030c': 3, '\u0300': 4}

def _match(syllable, text, diacritic):
    tone = 5
    si = 0
    ti = 0
    while si < len(syllable) and ti < len(text):
        if text[ti] in _diacritic_table:
            if tone != 5:
                return None
            tone = _diacritic_table[text[ti]]
            ti += 1
        else:
            if text[ti] != syllable[si]:
                return None
            si += 1
            ti += 1
    if si < len(syllable):
        return None
    if ti < len(text) and text[ti] in _diacritic_table:
        if tone != 5:
            return None
        tone = _diacritic_table[text[ti]]
        ti += 1
    if diacritic:
        return (text[:ti], text[ti:])
    return (syllable + str(tone), text[ti:])
    
def split(text, diacritic=False):
    text = [(text.lower(), [])]
    candidates = []
    while len(text) != 0:
        t, acc = text.pop()
        if len(t) == 0:
            candidates.append(acc)
            continue
        for c in _pinyin_syllables:
            res = _match(c, t, diacritic)
            if res != None:
                text.append((res[1], acc + [res[0]]))
    return candidates

if __name__ == '__main__':
    import util
    test_words = ['líyuè', 'guīzhōng', 'zhōnglí', 'xiānglíng', 'guāzào', 'suǒyǒu', 'cuòguò']
    test_words = [util.normalize_unicode(elt) for elt in test_words]
    for test in test_words:
        print(split(test))
        print(split(test, diacritic=True))
