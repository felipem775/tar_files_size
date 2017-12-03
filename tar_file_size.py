#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "FelipeM"
__version__ = "0.1"
__status__ = "Development"

import os
import argparse
import tarfile
import human2bytes

def filesInDir(path):
    fileList = []
    for root, subdirs, files in os.walk(path):
        for f in files:
            fileList.append(os.path.join(root,f))
    return sorted(fileList)

def sizeFile(file):
    return os.path.getsize(file)

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
    max_file_per_tar = human2bytes.human2bytes(args.size)
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
    
