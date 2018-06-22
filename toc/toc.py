############# UNFINISHED

# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 13:44:49 2018

@author: FL


title : skip first header and add toc here

update : if True, remove old toc

what is toc? with * or -

Parameters
----------

If TITLE, skip the first header and insert toc right below it.
If no TITLE, insert toc right at the beginning of the file.

If UPDATE, check for existing toc and overwrites it, keeping original headlines.
If no UPDATE, do not check.

What is considered a toc?
If there is any - or * leading in the first or second sections

References
----------
https://guides.github.com/features/mastering-markdown/

"""

import codecs
import fileinput


def parse_header(line):
    def level(x):
        try:
            return {
                '#': 1,
                '##': 2,
                '###': 3,
                '####': 4,
                '#####': 5,
                '######': 6
            }[x]
        except KeyError:
            return 0

    splitted = line.split(maxsplit=1)
    if len(splitted) > 1:    # a line like '##' does not count as a header
        return level(splitted[0]), splitted[1:][0]
    else:
        return 0, None


def is_list(line):
    first = line.split(maxsplit=1)
    return len(first) > 0 and (first[0] == '-' or first[0] == '*')


filename = 'rm.md'
contents = []
top_level = 7
title_line = 0
text = ''
toc_section = []
toc_line = 0
toc_state = 0
last_line = 0


def make_toc(filename='README.md', title=True, update=True):
    headers = []
    lists = []
    empty = []
    top_level = 7

    with codecs.open(filename, mode='r', encoding='utf8') as f:
        begin = end = 0
        for i, line in enumerate(f):
            line = line.lstrip()
            if len(line) > 0:
                if line[0] == '#':
                    result = parse_header(line)
                    if result[0] > 0:
                        headers.append((i+1, result[0], result[1]))
                        if (result[0] < top_level) and \
                           (not (title and len(headers) == 1)):
                            top_level = result[0]
                elif line[0] == '-' or line[0] == '*':
                    if is_list(line):
                        lists.append(i+1)
            else:
                empty.append(i+1)

    toc = ''
    last_indent = 0
    this_indent = 0
    if title and len(headers) > 0:
        headers = headers[1:]
    for h in headers:
        this_indent = min(h[1] - top_level, last_indent + 1)
        anchor = '.'.join(h[2].lower().split())
        toc += '    ' * this_indent + '- [' + h[2] + ']' + '(' + anchor + ')'
        last_indent = this_indent

    # write toc

    i = 1
    for line in fileinput.input(filename, inplace=1):
        if (not update) or i < begin or i > end:
            print(line.rstrip())
        if i == toc_line:
            print()
            print(text.rstrip())
        i += 1


with codecs.open(filename, mode='r', encoding='utf8') as f:
    skip_title = True
    for i, line in enumerate(f):
        line = line.lstrip()
        if len(line) > 0:
            if line[0] == '#':
                if skip_title:
                    skip_title = False
                    last_line = title_line = i + 1
                    print('ll = ', last_line)

                    continue

                result = parse(line)
                if result[0] > 0:
                    last_line = i + 1
#                    print('last_line = ', last_line)
                    contents.append((result[0], result[1]))
                    if toc_state == 1:
                        toc_state = 2
                    if result[0] < top_level:
                        top_level = result[0]
#                    print(i + 1, '[', result[0], ']', result[1], '(', toc_state, ')')
            elif len(contents) < 2 and toc_state < 2:
                first = line.split(maxsplit=1)[0]
                if first == '-' or first == '*':
                    toc_line = last_line
                    if len(toc_section) > 1:
                        toc_section.pop()
                    toc_section.append(i + 1)
                    toc_state = 1


    last_indent = 0
    this_indent = 0
    last_level = contents[0][0]
    for h in contents:
        this_indent = min((h[0] - top_level), last_indent + 1)
        text += '    ' * this_indent
        text += '- '
        text += h[1]
        last_indent = this_indent

# if title, toc_line = title_line

if toc_line == 0:
    toc_line = title_line

print('tocline = ', toc_line)

i = 1
for line in fileinput.input(filename, inplace=1):
    if len(toc_section) == 0 or i < toc_section[0] or i > toc_section[1]:
        print(line, end='')
    if i == toc_line:
        print()
        print(text.rstrip())
    i += 1



#print(contents)

