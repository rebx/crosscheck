#!/usr/bin/env python

import os
import sys
import signal
import argparse
import re

def find_pattern(pattern, filehandle):
    """
    find_pattern takes in a pattern and a file handle and searches for that
    pattern in that file
    """
    pattern = pattern.rstrip('\n')
    pat = re.compile(pattern)
    filehandle.seek(0)
    for line in filehandle.readlines():
        line = line.rstrip('\n')
        if pat.search(line):
            yield line
  
def parse_file(entries, scrape):
    """
    parse_file will get all the lines in the first file and search for them
    one by one on the second one
    """
    entriesfile = open(entries, 'r')
    scrapefile = open(scrape, 'r')
    for line in entriesfile.readlines():
        matches = find_pattern(line, scrapefile)
        for match in matches:
            print match
    
def match_files(entries, scrape,  nthreads=8):
    """
    calls parse_files to do the hard work
    """
    parse_file(entries, scrape)
  
def main():
    """
    main processing body
    """
    
    # set the signal straight away
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    description = """
      Processes two text files and finds common lines
    """
  
    usage = "%prog [source file] [file to grep]"
    progname = "crosscheck"
    nthreads = 8
    prs = argparse.ArgumentParser(prog=progname, description=description,
                                  usage=None)
    
    prs.add_argument('-n', '--num-threads', dest='nthreads', action='store',
                     help='The number of threads to use')
    (entries, scrape) =sys.argv[1:]
    print "%s finding entries in %s from %s" % (progname, scrape, entries)
    match_files(entries, scrape, nthreads)
  
if __name__ == '__main__':
    main()
