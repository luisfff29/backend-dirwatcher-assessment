#!/usr/bin/env python3
"""
Long Running Program with signal handling and logging
"""

import argparse
import time
import signal
import logging
import datetime
import os

__author__ = 'luisfff29'

# Create logger variable naming the logging as '__main__'
logger = logging.getLogger(__name__)

# Create an exit_flag to stop a infinite while loop
exit_flag = False


def create_parser():
    """
    Create a cmd line parser object with 2 flags and 2 argument definitions
    """
    parser = argparse.ArgumentParser(
        description='Watches a directory of text files for a magic string')
    parser.add_argument('path', help='Directory path to watch')
    parser.add_argument('magic', help='String to watch for')
    parser.add_argument('-e', '--ext',
                        action='store',
                        help='Text file extension to wach e.g. .txt, .log',
                        required=True)
    parser.add_argument('-i', '--interval',
                        action='store',
                        help='Number of seconds between polling',
                        default=1)
    return parser


def watch_directory(ext, interval, path, magic):
    """Look at directory and get a list of files from it"""
    # Copy of the dict to keep track of the directories
    # with their files
    copy_dict = {}

    while not exit_flag:
        try:
            # Keys of the dict are filenames and the values are (last line
            # number, magic text)
            dict_ = {x: scan_single_file(path, x, magic)
                     for x in os.listdir(path) if x.endswith(ext)}
        except FileNotFoundError:
            logger.error('Directory or file not found: {}'.format(
                os.path.abspath(path)))
            time.sleep(interval)
        else:
            # Loop through the dictionary
            for filename in dict_:
                detect_added_files(filename, dict_, copy_dict)
                detect_magic_text(path, filename, dict_, copy_dict)

            # Loop through the copy of the dictionary
            for filename in copy_dict:
                detect_removed_files(filename, dict_)
                # After a iterate through all of its files in the directory
                # make a copy of the original dict to the copy_dict
                copy_dict = dict_


def scan_single_file(p, f, m):
    """Open the file and search for the magic text returning the line number
    with the line matched"""
    with open(os.path.join(p, f)) as o:
        lines = o.readlines()
    for line in lines[::-1]:
        if m in line:
            return (len(lines) - lines[::-1].index(line), line)
    else:
        return None


def detect_added_files(f, d, c_d):
    """Report new files that are added to your dictionary with
    the proper extension"""
    if f not in c_d:
        logger.info('File added: ' + f)
        c_d[f] = None


def detect_removed_files(f, d):
    """After detect files and magic texts, find out if the file still
     exists in the directory, if not, report it and remove it"""
    if f not in d:
        logger.info('File removed: ' + f)


def detect_magic_text(p, f, d, c_d):
    """Report magic text when the copy_dict doesn't have yet the value
    of the file"""
    if c_d[f] != d[f]:
        logger.info('Magic text found: line {} of file {}'.format(
            d[f][0], os.path.abspath(os.path.join(p, f))))
        c_d[f] = d[f]


def start_banner(t):
    """Startup BANNER for a nice presentation and the time it started"""
    logger.info(
        '\n'
        '-------------------------------------------------------------------\n'
        '     Running {}\n'
        '     Started on {}\n'
        '-------------------------------------------------------------------\n'
        .format(__file__, t.isoformat())
    )


def end_banner(t):
    """Shutdown BANNER and the total time it was running"""
    # Result of the time since started running until it was over
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
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped
    here as well (SIGHUP?)
    Basically it just sets a global flag, and main() will exit it's loop
    if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    # log the associated signal name (the python3 way)
    logger.warning('Received OS process signal ' +
                   signal.Signals(sig_num).name)
    global exit_flag
    exit_flag = True


def main():
    # Hook these two signals from the OS ..
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(name)'
               '-12s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    logger.setLevel(logging.INFO)
    app_start_time = datetime.datetime.now()

    # Create a command-line parser object with parsing rules
    parser = create_parser()
    args = parser.parse_args()

    # Body of the program
    start_banner(app_start_time)

    watch_directory(args.ext, float(args.interval), args.path, args.magic)

    end_banner(app_start_time)


if __name__ == '__main__':
    main()
