#!/usr/bin/env python3
import argparse
import time
import signal


__author__ = 'luisfff29'

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


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped here as well (SIGHUP?)
    Basically it just sets a global flag, and main() will exit it's loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    # log the associated signal name (the python3 way)
    print('Received ' + signal.Signals(sig_num).name)
    global exit_flag
    exit_flag = True


def main():
    # parser = create_parser()
    # print(parser.parse_args())

    # Hook these two signals from the OS ..
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    while not exit_flag:
        try:
            print('Tick...')
            time.sleep(1)
            print('Tock...')
            time.sleep(1)
        except KeyboardInterrupt:
            print('Hey!!! DON\'T INTERRUPT MEEEE')
    print('I have shut down gracefully')


if __name__ == '__main__':
    main()
