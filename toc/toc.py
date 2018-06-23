# -*- coding: utf-8 -*-
"""
References
----------
https://guides.github.com/features/mastering-markdown/

"""

import codecs
import fileinput
import os.path
import shutil

from catch import catch


__all__ = ['auto_toc']


def parse_header(line):
    '''
    Parse a line to tell if it is a markdown header. Return a tuple of two:
    (level of header, contents of header). If not a header, returns (0, None).
    '''

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
    # a line that consists of only '#', like '###', does not count as a header
    if len(splitted) > 1:
        return level(splitted[0]), splitted[1:][0]
    else:
        return 0, None


def parse_list(line):
    '''
    Parse a line to tell if it is a markdown list. Return True or False.
    '''
    first = line.split(maxsplit=1)
    return len(first) > 0 and (first[0] == '-' or first[0] == '*')


@catch()
def auto_toc(filename, has_title, has_toc_header, toc_header, override):

    name, ext = os.path.splitext(filename)
    print('\nReading %s ...' % filename)
    if ext.lower() not in {'.markdown', '.mdown', '.mkdn', '.mkd', '.md'}:
        raise IOError('Expect a markdown file, but file extension is %s.'
                      % ext)
    copyname = name + '.bak'
    print('\nSaving a back-up copy to %s ...' % copyname)
    shutil.copyfile(filename, copyname)

    headers = []   # list of tuple of 3: [(line number, level, contents), ...]
    lists = []     # list of line numbers of markdown lists
    empty = []     # list of line number of empty lines
    top_level = 7  # top level among all headers, not counting title, toc

    # scan a markdown file for headers, lists, and empty lines
    print('\nScanning file for headers ...')
    with codecs.open(filename, mode='r', encoding='utf8') as f:
        for i, line in enumerate(f):
            line = line.lstrip()
            if len(line) > 0:
                if line[0] == '#':
                    result = parse_header(line)
                    if result[0]:
                        headers.append((i + 1, result[0], result[1]))
                elif line[0] == '-' or line[0] == '*':
                    if parse_list(line):
                        lists.append(i + 1)
            else:
                empty.append(i + 1)

    # get line number of title, if any
    title_line = 0
    if has_title and len(headers) > 0:
        print('\nReading title: %s ...' % headers[0][2][:10].rstrip())
        title_line = headers[0][0]
        headers = headers[1:]

    # get line number of header for toc, if any
    toc_line = title_line
    if has_toc_header and len(headers) > 0:
        print('\nReading TOC header: %s ...' % headers[0][2][:10].rstrip())
        toc_line = headers[0][0]
        headers = headers[1:]

    # get top level among all headers, if any (top level is smallest level)
    top_level = 1
    if len(headers) > 0:
        top_level = min(x[1] for x in headers)

    # prepare new toc header
    if toc_header is not None:
        print('\nPreparing new TOC header: %s ...' % toc_header)
        toc_header = '#' * top_level + ' ' + toc_header

    # decide where to remove, in order to override old toc
    to_remove = [x for x in lists
                 if x > toc_line and (len(headers) == 0 or x < headers[0][0])]

    # plan to remove the entire old toc area and all the following empty lines
    if toc_header is not None:
        to_remove = [toc_line] + to_remove
    if len(to_remove) > 0:
        to_remove = list(range(to_remove[0], to_remove[-1] + 1))
        while to_remove[-1] + 1 in empty:
            to_remove.append(to_remove[-1] + 1)
        print('\nDetected an existing TOC, from line %d to line %d ...' %
              (to_remove[0], to_remove[-1]))

    # prepare new toc
    toc = ''
    indent = last_indent = 0
    for h in headers:
        # try best to reflect toc structure while following markdown rules
        indent = min(h[1] - top_level, last_indent + 1)
        anchor = '#user-content-' + '-'.join(h[2].lower().split())
        toc += '\n%s- [%s](%s)\n' % ('    ' * indent, h[2].rstrip(), anchor)
        last_indent = indent

    # write file
    print('\nMaking / Updating TOC for %d headers ...' % len(headers))
    i = 1
    for line in fileinput.input(filename, inplace=1):
        # insert at the beginning, if applicable
        if toc_line == 0 and i == 1:
            if toc_header is not None:
                print(toc_header)
            print(toc)
        # remove old toc
        if override and (i in to_remove):
            pass
        else:
            print(line.rstrip())
        # insert after toc line, if applicable
        if i == toc_line:
            if toc_header is not None:
                print(toc_header)
            print(toc.rstrip())
        i += 1

    print('\nFinish ...')


if __name__ == '__main__':

    print('----- Make/Update Table of Contents (TOC) for Markdown Files -----')
    filename = input('Enter filename '
                     '(press ENTER for \'README.md\') : ')
    has_title = input('Has header for title '
                      '(press ENTER for YES, enter any key for no) ? ')
    has_toc_header = input('Has header for table of contents '
                           '(press ENTER for YES, enter any key for no) ? ')
    toc_header = input('Enter new TOC header '
                       '(press ENTER if none or no change) : ')
    override = input('Override any existing TOC '
                     '(press ENTER for YES, enter any key for no) ? ')

    params = [filename, has_title, has_toc_header, toc_header, override]
    default = ['README.md', True, True, None, True]
    otherwise = []

    for i in range(len(params)):
        if len(params[i]) == 0:
            print('set to default (%d) : ' % i, default[i])
            params[i] = default[i]

    params[1] = bool(params[1])
    params[2] = bool(params[2])
    params[4] = bool(params[4])

    auto_toc(*params)
