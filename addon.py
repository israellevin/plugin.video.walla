#!/usr/bin/python
# coding=utf-8

import sys
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])

import xbmcplugin
xbmcplugin.setContent(addon_handle, 'episodes')

import urlparse
args = urlparse.parse_qs(sys.argv[2][1:])
mode = args.get('mode', None)

from urllib import FancyURLopener, urlencode
class URLOpener(FancyURLopener):
    version = 'Mozilla/5.0 (X11; Linux i686; rv:31.0) Gecko/20100101 Firefox/31.0 Iceweasel/31.0'
urlopen = URLOpener().open
urlmake = lambda query: base_url + '?' + urlencode(query)

rooturl = 'http://nick.walla.co.il'
def getpage(url):
    if url.startswith('/'): url = rooturl + url
    elif not url.startswith('http://'): url = rooturl + '/' + url
    resets = 0
    for tries in range(5):
        try:
            page = urlopen(url).read()
            break
        except IOError:
            page = u''
    if isinstance(page, str): page = page.decode('windows-1255', 'replace')
    page = page.encode('utf-8')
    return page

import re
vidregexp = re.compile(
    'class="vitem.*?"',
    re.DOTALL
)
nextregexp = re.compile(
    '<a class="p_r" style="" href="(.+?)"'
)
def vidsfromseason(url):
    page = getpage(url)
    vids = vidregexp.findall(page)
    for nexturl in nextregexp.findall(page):
        vids += vidregexp.findall(getpage(nexturl))
    return vids

def vidsfromshow(showurl):
    return [vidsfromseason(url) for url in re.findall(
        'href="([^"]*)"[^>]*>[^<]*פרקים מלאים',
        getpage(showurl)
    )]

import xbmcgui
if mode is None:
    for show in re.findall(
        '<a href="([^"]+)" class="item right w3" style=".*?">([^<]+)</a>',
        getpage('/')
    ):
        xbmcplugin.addDirectoryItem(
            handle=addon_handle,
            url=urlmake({'mode': 'show', 'showurl': show[0]}),
            listitem=xbmcgui.ListItem(show[1]),
            isFolder=True
        )
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'show':
    print(vidsfromshow(args['showurl'][0]))

    xbmcplugin.addDirectoryItem(
        handle=addon_handle,
        url='/',
        listitem=xbmcgui.ListItem('Video')
    )
    xbmcplugin.endOfDirectory(addon_handle)
