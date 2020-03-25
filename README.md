# Dirwatcher

Long Running Program with signal handling and logging

## Objective:

- Create a long running program
- Demonstrate signal handling
- Demonstrate program logging
- Use exception handling to keep the program running
- Create and structure your own code repository using best practices

## Goal

The `dirwatcher.py` program should accept some command line arguments that will instruct it to monitor a given directory for text files that are created within the monitored directory. The `dirwatcher.py` program will continually search within all files in the directory for a 'magic' string which is provided as a command line argument. This can be implemented with a timed polling loop. If the magic string is found in a file, your program should log a message indicating which file and line number the magic text was found. Once a magic text occurrence has been logged, it should not be logged again unless it appears in the file as another subsequent line entry later on.

Files in the monitored directory may be added or deleted or appended at any time by other processes. The program should log a message when new files appear or other previously watched files disappear. Assume that files will only be changed by <u>appending</u> to them. That is, anything that has previously been written to the file will not change. Only new content will be added to the end of the file. It doesn't have to continually re-check sections of a file that it has already checked.

The program should terminate itself by catching SIGTERM or SIGINT (be sure to check a termination message). The OS will send a signal event to processes that it wants to terminate from the outside.

## How do I test this??

<b>Testing Program Operation</b>

Test thte dirwatcher program using TWO terminal windows. In the first window, start your Dirwatcher with various sets of command line arguments. Open a second terminal window and navigate to the same directory where the Dirwatcher is running, and follow at these procedures:

- Run Dirwatcher with non-existent directory -- Every polling interval, it should complain about the missing watch directory.
- Create the watched directory with mkdir -- Dirwatcher should stop complaining.
- Add an <b>empty</b> file with target extension to the watched directory -- Dirwatcher should report a new file added.
- Append some magic text to first line of the empty file -- Dirwatcher should report that some magic text was found on line 1, <b>only once</b>.
- Append a few other non-magic text lines to the file and then another line with two or more magic texts -- Dirwatcher should correctly report the line number just once (don't report previous line numbers)
- Add a file with non-magic extension and some magic text -- Dirwatcher should not report anything
- Delete the file containing the magic text -- Dirwatcher should report the file as removed, <b>only once</b>.
- Remove entire watched directory -- Dirwatcher should revert to complaining about a missing watch directory, every polling interval.

<b>Testing the Signal Handler</b>

To test the OS signal handler part of the Dirwatcher, send a SIGTERM to the program from a separate shell window.

1. While the Dirwatcher is running, open a new shell terminal.
2. Find the process id (PID) of the dirwatcher. PID is the first column listed from the ps utility.
3. Send a SIGTERM to the Dirwatcher
4. The signal handler within the python program should be called. The code should exit gracefully with a Goodbye message ...

## Credits

This assignment was inspired by the story of [The Cuckoo's Egg](https://en.wikipedia.org/wiki/The_Cuckoo%27s_Egg)
