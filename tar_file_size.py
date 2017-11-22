#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "FelipeM"
__version__ = "0.1"
__status__ = "Development"

import os
import argparse
import tarfile

def filesInDir(path):
    fileList = []
    for root, subdirs, files in os.walk(path):
        for f in files:
            fileList.append(os.path.join(root,f))
    return sorted(fileList)

def sizeFile(file):
    return os.path.getsize(file)

SYMBOLS = {
    'customary'     : ('B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'),
    'customary_ext' : ('byte', 'kilo', 'mega', 'giga', 'tera', 'peta', 'exa',
                       'zetta', 'iotta'),
    'iec'           : ('Bi', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi'),
    'iec_ext'       : ('byte', 'kibi', 'mebi', 'gibi', 'tebi', 'pebi', 'exbi',
                       'zebi', 'yobi'),
}
def human2bytes(s):
    """
    http://code.activestate.com/recipes/578019-bytes-to-human-human-to-bytes-converter/

    Attempts to guess the string format based on default symbols
    set and return the corresponding bytes as an integer.
    When unable to recognize the format ValueError is raised.

      >>> human2bytes('0 B')
      0
      >>> human2bytes('1 K')
      1024
      >>> human2bytes('1 M')
      1048576
      >>> human2bytes('1 Gi')
      1073741824
      >>> human2bytes('1 tera')
      1099511627776
      >>> human2bytes('0.5kilo')
      512
      >>> human2bytes('0.1  byte')
      0
      >>> human2bytes('1 k')  # k is an alias for K
      1024
      >>> human2bytes('12 foo')
      Traceback (most recent call last):
          ...
      ValueError: can't interpret '12 foo'
    """
    if s.isdigit():
        return int(s)
    init = s
    num = ""
    while s and s[0:1].isdigit() or s[0:1] == '.':
        num += s[0]
        s = s[1:]
    num = float(num)
    letter = s.strip()
    for name, sset in SYMBOLS.items():
        if letter in sset:
            break
    else:
        if letter == 'k':
            # treat 'k' as an alias for 'K' as per: http://goo.gl/kTQMs
            sset = SYMBOLS['customary']
            letter = letter.upper()
        else:
            raise ValueError("can't interpret %r" % init)
    prefix = {sset[0]:1}
    for i, s in enumerate(sset[1:]):
        prefix[s] = 1 << (i+1)*10
    return int(num * prefix[letter])

def split_in_max_size(max_size, files):
    lists_files = []
    count = 0
    current_tar_files = []
    for f in files:
        filesize = os.path.getsize(f)
        if filesize + count > max_size:
            lists_files.append(current_tar_files)
            current_tar_files = []
            count = 0
        current_tar_files.append(f)
        count += filesize
    lists_files.append(current_tar_files)
    return lists_files[1:]

def do_tar(filename, files):
    tar = tarfile.open(filename, "w")
    for f in files:
        tar.add(f)
    tar.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path of files", type=str)
    parser.add_argument("size", help="max size per tar", type=str)
    parser.add_argument("output", help="ouput file name", type=str)
    args = parser.parse_args()

    # Get parameters
    max_file_per_tar = human2bytes(args.size)
    path = args.path
    output = args.output 
    
    # Get list of files
    complete_list_files = filesInDir(path)
    # Do a list of files in tar
    list_tar = split_in_max_size(max_file_per_tar, complete_list_files)

    # Values for naming tar files
    number_total_tar = len(list_tar)
    number_current_tar = 1
    # Do tar files
    for l in list_tar:
        tar_filename = "{0}.{1:02d}of{2:02d}.tar".format(output,number_current_tar, number_total_tar)
        number_current_tar += 1
        do_tar(tar_filename, l)
    
