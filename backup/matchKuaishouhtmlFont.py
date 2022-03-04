import re
import requests

from cStringIO import StringIO
from fontTools.ttLib import TTFont

_pat_font_url = re.compile("'(//static.yximgs.com/udata/pkg/kuaishou-front-end-live/fontscn_([0-9a-f]{32}).+?woff)'")
_pat_font = re.compile('&#x[0-9a-f]{4};')

maps = {}


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'Host': 'live.kuaishou.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
}


def get_font_regx(digest, font_url):
    if digest in maps:
        return maps[digest]
    resp = requests.get(font_url)
    font = TTFont(StringIO(resp.content))

    for k, v in font.getBestCmap().items():
        if v.startswith('uni'):
            mappings['&#x{:x}'.format(k)] = unichr(int(v[3:], 16))
        else:
            mappings['&#x{:x}'.format(k)] = v

    def callback(regx):
        return mappings.get(regx.group(0), regx.group(0))
    maps[digest] = callback
    return callback

if __name__ == '__main__':
    resp = requests.get('https://live.kuaishou.com/profile/3xkerh5gjsd76me', headers=headers)
    #print(resp.text)
    url, digest = _pat_font_url.search(resp.text).groups()
    font_url = 'https:' + url
    callback = get_font_regx(digest, font_url)
    text = _pat_font.sub(callback, resp.text)
    print(text)

