#!/usr/bin/env python3
import argparse

__author__ = 'luisfff29'


def create_parser():
    parser = argparse.ArgumentParser(
        description='Watches a directory of text files for a magic string')
    parser.add_argument('path', help='Directory path to watch')
    parser.add_argument('magic', help='String to watch for')
    parser.add_argument('-e', '--ext', action='store',
                        help='Text file extension to wach e.g. .txt, .log')
    parser.add_argument('-i', '--interval', action='store',
                        help='Number of seconds between polling')
    return parser


def main():
    parser = create_parser()
    print(parser.parse_args())


if __name__ == '__main__':
    main()
