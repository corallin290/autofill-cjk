import re
import unicodedata

_TAG_RE = re.compile(r'<[^>]+>')
def remove_html_tags(text):
    return _TAG_RE.sub('', text)

def normalize_unicode(text):
    return unicodedata.normalize('NFKD', text)
