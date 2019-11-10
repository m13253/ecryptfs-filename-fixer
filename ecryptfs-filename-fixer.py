#!/usr/bin/env python3

# ecryptfs-filename-fixer
# Copyright (C) 2019  Star Brilliant
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import unicodedata


def escape_path(path):
    return path.replace("'", "'\\''")


def walk(curdir, path):
    for segment, child in curdir.items():
        if len(segment.encode('utf-8', 'replace')) > 143:
            norm_segment = unicodedata.normalize('NFC', segment)
            new_segment = norm_segment
            trimmed = False
            segment_split = segment.rsplit('.', 1)
            if len(segment_split) == 2 and len(segment[0].encode('utf-8', 'replace')) + len(segment_split[1].encode('utf-8', 'replace')) <= 139:
                while len((new_segment + '….' + segment_split[1]).encode('utf-8', 'replace')) > 143:
                    new_segment = new_segment[:-1]
                    trimmed = True
                if trimmed:
                    new_segment += '…'
                new_segment += '.'
                new_segment += segment_split[1]
            else:
                while len(new_segment.encode('utf-8', 'replace')) > 140:
                    new_segment = new_segment[:-1]
                    trimmed = True
                new_segment += '…'
            if path:
                print("mv -nv '{}/{}' '{}/{}'".format(escape_path(path), escape_path(segment), escape_path(path), escape_path(new_segment)))
            else:
                print("mv -nv '{}' '{}'".format(escape_path(segment), escape_path(new_segment)))
            record_file = norm_segment
            trimmed = False
            while len((record_file).encode('utf-8', 'replace')) > 130:
                record_file = record_file[:-1]
                trimmed = True
            if trimmed:
                record_file += '…'
            record_file += '.orig_name'
            if path:
                print("echo -n '{}' >'{}/{}'".format(escape_path(norm_segment), escape_path(path), escape_path(record_file)))
                walk(child, path + '/' + new_segment)
            else:
                print("echo -n '{}' >'{}'".format(escape_path(norm_segment), escape_path(record_file)))
                walk(child, new_segment)
        elif path:
            walk(child, path + '/' + segment)
        else:
            walk(child, segment)


def main():
    root = {}
    for line in sys.stdin:
        line = line.rstrip('\r\n')
        path = []
        for segment in line.split('/'):
            if segment == '.':
                continue
            elif segment == '..':
                if len(path) != 0:
                    del path[len(path) - 1]
                else:
                    path.append('..')
            else:
                path.append(segment)
        curdir = root
        for segment in path:
            if segment not in curdir:
                curdir[segment] = {}
            curdir = curdir[segment]
    walk(root, '')


if __name__ == '__main__':
    main()
