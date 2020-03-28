#!/usr/bin/env python3
import argparse
import time
import signal
import logging
import datetime
import os


__author__ = 'luisfff29'


logger = logging.getLogger(__name__)


exit_flag = False


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


def watch_directory(ext, interval, path, magic):
    copy_dict = {}

    while True:
        try:
            dict_ = {x: scan_single_file(path, x, magic)
                     for x in os.listdir(path) if x.endswith(ext)}
        except FileNotFoundError:
            logger.error('Directory or file not found: {}'.format(
                os.path.abspath(path)))
            time.sleep(interval)
        else:
            for filename in dict_:
                detect_added_files(filename, dict_, copy_dict)
                detect_magic_text(filename, dict_, copy_dict)

            for filename in copy_dict:
                detect_removed_files(filename, dict_)
                copy_dict = dict_


def scan_single_file(p, f, m):
    with open(os.path.join(p, f)) as o:
        lines = o.readlines()
    for line in lines[::-1]:
        if m in line:
            return (len(lines) - lines[::-1].index(line), line)
    else:
        return None


def detect_added_files(f, d, c_d):
    if f not in c_d:
        logger.info('File added: ' + f)
        c_d[f] = None


def detect_removed_files(f, d):
    if f not in d:
        logger.info('File removed: ' + f)


def detect_magic_text(f, d, c_d):
    if c_d[f] != d[f]:
        logger.info('Magic text found: line {} of file {}'.format(
            d[f][0], os.path.abspath(f)))
        c_d[f] = d[f]


def start_banner(t):
    logger.info(
        '\n'
        '-------------------------------------------------------------------\n'
        '     Running {}\n'
        '     Started on {}\n'
        '-------------------------------------------------------------------\n'
        .format(__file__, t.isoformat())
    )


def end_banner(t):
    uptime = datetime.datetime.now() - t

    logger.info(
        '\n'
        '-------------------------------------------------------------------\n'
        '     Stopped {}\n'
        '     Uptime was {}\n'
        '-------------------------------------------------------------------\n'
        .format(__file__, str(uptime))
    )


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped here as well (SIGHUP?)
    Basically it just sets a global flag, and main() will exit it's loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    # log the associated signal name (the python3 way)
    # print('Received ' + signal.Signals(sig_num).name)
    global exit_flag
    exit_flag = True


def main():

    # Hook these two signals from the OS ..
    # signal.signal(signal.SIGINT, signal_handler)
    # signal.signal(signal.SIGTERM, signal_handler)
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    logger.setLevel(logging.INFO)
    app_start_time = datetime.datetime.now()

    parser = create_parser()
    args = parser.parse_args()

    start_banner(app_start_time)

    watch_directory(args.ext, float(args.interval), args.path, args.magic)

    end_banner(app_start_time)


if __name__ == '__main__':
    main()
