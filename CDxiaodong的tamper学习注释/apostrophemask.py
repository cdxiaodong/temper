#!/usr/bin/env python

"""
Copyright (c) 2006-2021 sqlmap developers (https://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

from lib.core.enums import PRIORITY
##引用了lib.core.enums这个库。这个库在\sqlmap\lib\core\enums.py上

__priority__ = PRIORITY.LOWEST
##调用priority这个库指定最低线程

def dependencies():
    pass
##dependencies函数，对tamper脚本支持/不支持使用的环境进行声明，可以为空。如上

def tamper(payload, **kwargs):
    ##temper函数，temper是整个脚本的主题。主要用于替换原本的payload，返回值位替换后的payload
    ##kwargs位官方提供的47个temper脚本之一。用于更改http-header
    """
    Replaces apostrophe character (') with its UTF-8 full width counterpart (e.g. ' -> %EF%BC%87)

    References:
        * http://www.utf8-chartable.de/unicode-utf8-table.pl?start=65280&number=128
        * https://web.archive.org/web/20130614183121/http://lukasz.pilorz.net/testy/unicode_conversion/
        * https://web.archive.org/web/20131121094431/sla.ckers.org/forum/read.php?13,11562,11850
        * https://web.archive.org/web/20070624194958/http://lukasz.pilorz.net/testy/full_width_utf/index.phps

    >>> tamper("1 AND '1'='1")
    '1 AND %EF%BC%871%EF%BC%87=%EF%BC%871'
    """
    ##绕过参考文件和演示示例

    return payload.replace('\'', "%EF%BC%87") if payload else payload
    ##真正实现绕过的代码，对引号内容进行utf-8格式编码(%EF%BC%87)
    