# -*- coding: utf-8 -*-
"""
It is a shame for the fileinput module in Python's Standard Library that it
does not allow inplace editing with specified encoding.

> You cannot use inplace and openhook together.

This function, adapted from by @robru on stackoverflow, helps to achieve this.

References
----------

https://docs.python.org/3.6/library/fileinput.html#module-fileinput

https://stackoverflow.com/questions/25203040/fileinput-inplace-filtering-encoding
"""

# Date: 18/06/24 = Sun

# Author: Fu Lei <lei dot fu at connect dot ust dot hk>

import os
import os.path
import shutil
import codecs


def inplace(file, encoding='utf-8', backup=True):
    if backup:
        name, ext = os.path.splitext(file)
        shutil.copy(file, name + '.bak')
    temp = name + '.tmp'
    with codecs.open(file, 'r', encoding=encoding) as old, \
            codecs.open(temp, 'w', encoding=encoding) as new:
            for line in old:
                yield line, new
    os.remove(file)
    os.rename(temp, file)


# test: add line numbers in Chinese to each line of a given file in UTF-8
if __name__ == '__main__':
    file = input('Filename ? ')
    i = 1
    for line, new in inplace(file):
        line = '第' + str(i) + '行：' + line
        new.write(line)
        i += 1
