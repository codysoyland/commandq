commandq 0.1
============

Create simple command queue invoker/worker processes with UNIX pipes and file locks.

usage
-----

To start a worker process:

    $ ./commandq.py worker

To start an invoker process:

    $ ./commandq.py invoker

The invoker gives you a shell to enter commands into the queue which worker processes will run.

license
-------

BSD v2 - Use however you please
