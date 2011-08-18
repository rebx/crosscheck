#!/usr/bin/env python

"""
Name: crosscheck.py
Author: rebX
Description: A multiline grep tool using generators
"""

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

    usage = "%(prog)s [source file] [file to grep]"
    progname = "crosscheck"
    nthreads = 8
    prs = argparse.ArgumentParser(prog=progname, description=description,
                                  usage=usage)

    prs.add_argument('-n', '--num-threads', dest='nthreads', action='store',
                    type=int, help='The number of threads to use')
    try:
        (entries, scrape) =sys.argv[1:]
        if os.path.exists(entries) == False:
            raise IOError(entries)
        if os.path.exists(scrape) == False:
            raise IOError(scrape)
    except ValueError, TypeError:
        print >> sys.stderr, progname + ' expects two entries: '
        prs.print_help()
        sys.exit(1)
    except IOError:
        print "Non-existing file: ", sys.exc_info()[1]
        prs.print_help()
        sys.exit(1)

    print "%s finding entries in %s from %s" % (progname, scrape, entries)
    match_files(entries, scrape, nthreads)

if __name__ == '__main__':
    main()
