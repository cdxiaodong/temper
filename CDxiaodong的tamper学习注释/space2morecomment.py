#!/usr/bin/env python

"""
Copyright (c) 2006-2021 sqlmap developers (https://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

from lib.core.compat import xrange
from lib.core.enums import PRIORITY

__priority__ = PRIORITY.LOW

def dependencies():
    pass

def tamper(payload, **kwargs):
    """
    Replaces (MySQL) instances of space character (' ') with comments '/**_**/'

    Tested against:
        * MySQL 5.0 and 5.5

    Notes:
        * Useful to bypass weak and bespoke web application firewalls

    >>> tamper('SELECT id FROM users')
    'SELECT/**_**/id/**_**/FROM/**_**/users'
    """

    retVal = payload

    if payload:
        retVal = ""
        quote, doublequote, firstspace = False, False, False
        ##声明变量“引用”“双引用”“一维”
        for i in xrange(len(payload)):
            if not firstspace:
                if payload[i].isspace():
                    #isspace() 方法检测字符串是否只由空格组成
                    firstspace = True
                    retVal += "/**_**/"
                    #那就给这个点位的字符串加上/**_**/
                    continue

            elif payload[i] == '\'':
                quote = not quote

            elif payload[i] == '"':
                doublequote = not doublequote

            elif payload[i] == " " and not doublequote and not quote:
                retVal += "/**_**/"
                #排除冗余项
                continue

            retVal += payload[i]

    return retVal
