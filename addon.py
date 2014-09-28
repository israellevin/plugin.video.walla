#!/usr/bin/python

def toutf(name):
    if isinstance(name, str): name = name.decode('windows-1255', 'replace')
    return name.encode('utf-8')

import sys
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])

import xbmcplugin
xbmcplugin.setContent(addon_handle, 'episodes')

import urlparse
args = urlparse.parse_qs(sys.argv[2][1:])
mode = args.get('mode', None)

from urllib import urlopen, urlencode
def build_url(query):
    return base_url + '?' + urlencode(query)

import re
import xbmcgui
if mode is None:
    for show in re.findall(
        '<a href="([^"]+)" class="item right w3" style="">([^<]+)</a>',
        urlopen('http://nick.walla.co.il/').read()
    ):
        xbmcplugin.addDirectoryItem(
            handle=addon_handle,
            url=build_url({'mode': 'show', 'showurl': show[0]}),
            listitem=xbmcgui.ListItem(toutf(show[1])),
            isFolder=True
        )
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'show':
    showurl = args['showurl'][0]
    xbmcplugin.addDirectoryItem(
        handle=addon_handle,
        url=showurl,
        listitem=xbmcgui.ListItem('Video')
    )
    xbmcplugin.endOfDirectory(addon_handle)

seasonsregexp = re.compile(
    '<div class=" topbrd"></div><a href="([^"]+)"[^>]*>([^<]+)'
)
nextregexp = re.compile(
    'class="in_blk p_r"\sstyle=""\shref="(.*?)"'
)
