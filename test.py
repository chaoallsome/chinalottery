#!/usr/bin/env python
#coding: utf-8 
"""
    test.py
    xx/xx/20xx
    ~~~~~~~~

    Description of test.py
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

USAGE = """
.py usage...
"""

def main(argv):
    try:
        opts, args = getopt.gnu_getopt(argv[1:], "h", ["help"])

        for o, a in opts:
            if o in ("-h", "--help"):
                print USAGE

    except getopt.GetoptError:
        print >> sys.stderr, USAGE
        return 2

if __name__ == '__main__':
    sys.exit(main(sys.argv))