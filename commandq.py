#!/usr/bin/env python

import time
import os
import sys
import fcntl
from contextlib import contextmanager

@contextmanager
def acquire_lock():
    with open('lockfile', 'r+') as lockfile:
        fcntl.lockf(lockfile.fileno(), fcntl.LOCK_EX)
        yield

def invoker(args, options):
    # TODO: raw_input only works for interactive mode. we also would like to
    # invoke with a command list in a file or by piping commands into stdin.
    while True:
        try:
            command = raw_input('$ ')
        except EOFError:
            break
        if command:
            with acquire_lock():
                with open('queue', 'w') as queue:
                    queue.write(command + '\n')
    return 0

def worker(args, options):
    while True:
        with open('queue', 'r') as queue:
            with acquire_lock():
                command = queue.readline()[:-1] # chop off \n
        if command:
            print 'RUNNING:', command
            os.system(command)
            try:
                os.wait()
            except:
                pass
    return 0

def setup_fs():
    if not os.path.exists('lockfile'):
        open('lockfile', 'w').close()
    if not os.path.exists('queue'):
        os.mkfifo('queue')

def main(args, options):
    setup_fs()
    if not args:
        print('Required argument: `invoker` or `worker`')
        return 0
    if args[0] == 'invoker':
        print('Starting invoker...')
        return invoker(args, options)
    elif args[0] == 'worker':
        print('Starting worker...')
        return worker(args, options)
    else:
        print('Invalid command.')

if __name__ == '__main__':
    exit(main(sys.argv[1:], {}))
