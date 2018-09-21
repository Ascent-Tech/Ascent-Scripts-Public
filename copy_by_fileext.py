"""
Script that can be used to extract .p4d files from all immediate subdirectories. 
Basically, for when we're trying to grab all the project data from our tablet.

Author: David Fairbairn
Date: September 2018
 
"""
import sys
import os
from shutil import copy2

def usage():
    print("Usage:\npython {0} <srch_dir> <save_dir> <file_ext>".format(sys.argv[0]))

def find_files(srch_dir, save_dir, file_ext):
    try:
        #print(os.listdir(srch_dir))
        for i in os.listdir(srch_dir):
            dir_i = srch_dir + i
            if os.path.isdir(dir_i):
                #print('directory: {0}'.format(dir_i))
                for j in os.listdir(dir_i):
                    fname = dir_i + '/' + j;
                    if os.path.splitext(fname)[1] == ".p4d":
                        print('found a {0} file! {1}'.format(file_ext, fname))
                        copy2(fname, save_dir)
    except Exception as e: # could handle specific errors in future
        print("Error: {0}".format(e))

def main():
    if len(sys.argv) != 4:
        usage()
        exit()
    find_files(sys.argv[1], sys.argv[2], sys.argv[3])    

if __name__=="__main__":
    main()
