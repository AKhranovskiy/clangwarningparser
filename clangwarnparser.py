#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import os
import json
from collections import namedtuple

RX_FILENAME = r'(?P<filename>(?:/[\w\.\-\_]+)+\.\w+)' +\
              r'\:(?P<line>\d+)\:(?P<pos>\d+)'
RX_WARNING = r'warning: (?P<msg>.+?) \[(?P<name>[\w\d\.\-]+)\]$'

Warning = namedtuple('Warning', 'file, line, pos, type, msg')


def get_normal_path(path, base):
    return os.path.relpath(path, base)


def main(logname, basepath, output):
    output.write('[\n')
    first = True
    with open(logname, 'r') as log:
        re_filename = re.compile(r'^'+RX_FILENAME)
        re_warning = re.compile(RX_WARNING)
        for line in log:
            filename = re_filename.search(line)
            warning = re_warning.search(line)
            if filename and warning:
                path = get_normal_path(filename.group('filename'), basepath)
                if not first:
                    output.write(',\n')
                output.write(json.dumps(
                    Warning(
                        path,
                        int(filename.group('line')),
                        int(filename.group('pos')),
                        warning.group('name'),
                        warning.group('msg'))._asdict()))
                first = False
    output.write('\n]\n')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("No input is specified")
        exit(1)
    buildlog = sys.argv[1]
    basepath = '/Users/khranovs/work/git/dev-framework/'
    main(buildlog, basepath, sys.stdout)
