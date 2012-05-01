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
import logging
import logging.config

USAGE = """
.py usage...
"""

def main(argv):
	pass

if __name__ == '__main__':
    logging.config.fileConfig("logging.conf")
    #create logger
    logger = logging.getLogger("simpleExample")
     
    #"application" code
    logger.debug("debug message")
    logger.info("info message")
    logger.warn("warn message")
    logger.error("error message")
    logger.critical("critical message")