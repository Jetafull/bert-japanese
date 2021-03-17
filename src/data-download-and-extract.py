#!/usr/bin/env python3

import configparser
import os
import subprocess
import sys
from urllib.request import urlretrieve
from pathlib import Path


CURDIR = Path(__file__).parent.parent.absolute()
WORKDIR = CURDIR.parent
CONFIGPATH = CURDIR / "config.ini"
config = configparser.ConfigParser()
config.read(CONFIGPATH)

FILEURL = config['DATA']['FILEURL']
FILEPATH = WORKDIR.joinpath(config['DATA']['FILEPATH']).as_posix()
EXTRACTDIR = WORKDIR.joinpath(config['DATA']['TEXTDIR']).as_posix()


def reporthook(blocknum, blocksize, totalsize):
    '''
    Callback function to show progress of file downloading.
    '''
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%5.1f%% %*d / %d" % (
            percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
        if readsofar >= totalsize:  # near the end
            sys.stderr.write("\n")
    else:  # total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))


def download():
    urlretrieve(FILEURL, FILEPATH, reporthook)


def extract():
    subprocess.call(['python3', 
                    WORKDIR.joinpath('wikiextractor', 'WikiExtractor.py').as_posix(),
                    FILEPATH, "-o={}".format(EXTRACTDIR)])


def main():
    download()
    extract()


if __name__ == "__main__":
    main()
