#!/usr/bin/env python

"""
Copyright (c) 2006-2021 sqlmap developers (https://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

import os

from lib.core.common import singleTimeWarnMessage
from lib.core.enums import DBMS
from lib.core.enums import PRIORITY

__priority__ = PRIORITY.LOWEST

def dependencies():
    singleTimeWarnMessage("tamper script '%s' is only meant to be run against %s" % (os.path.basename(__file__).split(".")[0], DBMS.ACCESS))
##dependencies对tamper脚本支持/不支持使用的环境进行声明,主要是起提示作用
##singleTimeWarnMessage用于在控制台中打印出警告信息
##此tamper '%s' 只针对 %s" 
##(os.path.basename(__file__).split(".")[0],标准代码。就是说dependencie的格式代码
##DBMS.MYSQL 这个参数代表的是 Mysql

def tamper(payload, **kwargs):
    """
    Appends (Access) NULL byte character (%00) at the end of payload

    Requirement:
        * Microsoft Access

    Notes:
        * Useful to bypass weak web application firewalls when the back-end
          database management system is Microsoft Access - further uses are
          also possible

    Reference: http://projects.webappsec.org/w/page/13246949/Null-Byte-Injection

    >>> tamper('1 AND 1=1')
    '1 AND 1=1%00'
    """

    return "%s%%00" % payload if payload else payload
    ##在最后加上%00
