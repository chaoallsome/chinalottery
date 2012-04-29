#!/usr/bin/env python
#coding: utf-8 
"""
    historyFetcher.py
    xx/xx/20xx
    ~~~~~~~~

    Description of historyFetcher.py
    Copyright
"""

__version__ = ''
__author__ = 'HaiBin Fu <haibinfu@gmail.com>'
__url__ = 'https://plus.google.com/116482646689120533058'
__license__ = ''
__docformat__ = 'restructuredtext'
__all__ = []

import sys
import getopt
import re
import HTMLParser
import urllib


USAGE = """
.py usage...
"""

#http://kaijiang.zhcw.com/zhcw/html/ssq/list.html
u'''从中彩网的页面抓取双色球开奖数据'''
class HistoryFetcher(HTMLParser.HTMLParser):
    selected = ('table','tr','td','em','strong','p')
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
    def reset(self):
        HTMLParser.HTMLParser.reset(self)
        self._level_stack=[]
        self.item = []
        self.items = []

    def handle_starttag(self,tag,attrs):
        if tag in HistoryFetcher.selected:
            self._level_stack.append(tag)

    def handle_endtag(self,tag):
        if self._level_stack and tag in HistoryFetcher.selected and tag == self._level_stack[-1]:
            self._level_stack.pop()

    def handle_data(self,data):
        p = re.compile('[0-9]+')
        q = re.compile('\d\d\d\d-\d\d-\d\d')
        if "/".join(self._level_stack) >= 'table/tr/td' and p.match(data) and not 'p' in self._level_stack:
            if len(self.item) < 12:
                if len(self.item) == 9 and q.match(data):
                    self.item = []
                self.item.append(data)
            if len(self.item) == 12:
         #       print self.item
                self.items.append(self.item)
                self.item = []

if __name__ == '__main__':
	his = HistoryFetcher()
	urlStr = "http://kaijiang.zhcw.com/zhcw/html/ssq/list.html"
	content = urllib.urlopen(urlStr).read()
	his.feed(content)
	print(his.items)
	
    