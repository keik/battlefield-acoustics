#!/usr/bin/env python

import argparse
import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
logger.addHandler(handler)


def main(filepath,
         rate,
         bufsize,
         win,
         shift):

    logger.debug(1)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process real-time HPSS and plotting.')
    parser.add_argument('filepath', nargs='?',
                        help="""
                        File path to analyze. If not specified, analyze mic input
                        """)
    parser.add_argument('-r', '--rate', dest='rate', default=44100,
                        help="""
                        Frame rate to read audio. Default value is 44100
                        """)
    parser.add_argument('-b', '--bufsize', dest='bufsize', default=1024,
                        help="""
                        Frames count to process fft per buffer. Default value is 1024
                        """)
    parser.add_argument('-w', '--win', dest='win', default='hamming',
                        help="""
                        Window function. Select from `hamming`, `hanning`, or `none`.
                        Default value is `hamming
                        """)
    parser.add_argument('-s', '--shift', dest='shift', default=256,
                        help="""
                        Shift size for window function. Default value is 256
                        """)
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help="""
                        Run as verbose mode
                        """)

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)

    main(args.filepath,
         int(args.rate),
         int(args.bufsize),
         args.win,
         int(args.shift))
