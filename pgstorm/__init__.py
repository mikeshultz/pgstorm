#!/bin/env python
#
# pgstorm
#
# Load testing for PostgreSQL
#
################################################################################
import sys
import time
import argparse
import psycopg2
import logging
from typing import Callable
from threading import Thread

log = logging.getLogger(__name__)


class Test(object):
    """ Single pg connection and query """

    def __init__(self, test_input):

        self.sql = test_input.get('sql')
        self.dsn = test_input.get('connection_string')
        self.handler = test_input.get('handler')
        self.type = test_input.get('test_type')
        self.value = test_input.get('check_value')
        self.result = None
        self._connection = None
        self._cursor = None

    def _connect(self):
        """ Connect to the server """

        log.debug("Connecting to %s" % self.dsn)

        self._connection = psycopg2.connect(self.dsn)
        self._cursor = self._connection.cursor()

    def _execute(self):
        """ Run the SQL """

        log.debug("Executing SQL")

        return self._cursor.execute(self.sql)

    def _disconnect(self):
        """ Commit and disconnect """

        log.debug("Committing transaction")

        self._connection.commit()

        log.debug("Disconnecting")
        
        self._cursor.close()
        self._connection.close()

    def run(self):
        """ Run the test """

        log.debug("Starting test")

        self._connect()
        self._execute()
        self.result = self._cursor.fetchall()
        self._disconnect()

        log.debug("Test complete")

        self.handler(self.result, self.type, self.value)

def result_handler(res: list, test_type: str, check_value: str = None):
    try:
        if test_type:
            if test_type == 'M':
                assert res is not None
                assert type(res) == list
                assert len(res) > 0
            elif test_type == 'N':
                assert res is not None
                assert type(res) == list
                assert len(res) == int(check_value)
            elif test_type == 'E':
                assert res is not None
                assert type(res) == list
                assert str(res[0][0]) == check_value
            else:
                raise Exception("Unknown test type")
        print('.', end='')
    except AssertionError:
        #log.exception("Test failed")
        print('E', end='')
    sys.stdout.flush()

def new_thread(test_input: dict):
    """ Setup the Test object and run it """

    t = Test(test_input)
    t.run()
    return t

def generate_threads(thread_count, test_input: dict, delay):
    """ Generate N threads """

    threads = [None for i in range(0, thread_count-1)]

    # Cycle through thread list and look for None threads
    while True:

        for i in range(len(threads)):
            
            if threads[i] is None or not threads[i].is_alive():

                log.info("Thread %s recycled." % i)

                threads[i] = Thread(target=new_thread, args=(test_input,))
                threads[i].start()

        time.sleep(delay)

def main():

    parser = argparse.ArgumentParser(description='PostgreSQL load testing.')
    parser.add_argument('connection_string', default=25, type=str, metavar='DSN',
                        help='pg connection string (default: postgresql://localhost:5432/postgres)')
    parser.add_argument('-t', '--threads', metavar='N', type=int, 
                        help='amount of threads to start')
    #parser.add_argument('-c', '--connections', default=25, type=int,
    #                    help='threads per connection')
    parser.add_argument('-s', '--sql', type=argparse.FileType('r'), 
                        default=sys.stdin, help='sql file to run(or stdin)')
    parser.add_argument('-d', '--delay', type=float, default=0.05, 
                        help='thread health check delay in seconds(default: 0.05)')
    parser.add_argument('-l', '--log-level', type=str, default='WARNING',
                        dest='level', help='log level(default: WARNING)')
    parser.add_argument('-y', '--type', type=str, default='M',
                        dest='type', help="""test type
                        M - Must have results, 
                        N - Must return --value rows, 
                        E - Equal too --value""")
    parser.add_argument('-v', '--value', type=str, dest='value', 
                        help='value comparison for test type')
    args = parser.parse_args()

    # Argument sanity checks
    if args.type:
        if args.type in {'N', 'E'}:
            if not args.value:
                raise Exception("--value must be set for this test type")
        elif args.type == 'M':
            if args.value:
                raise Exception("--value must not be set for this test type")
                
    # Read in the sql file/stdin
    sql = args.sql.read()
    # Setup logger
    logging.basicConfig(level=getattr(logging, args.level.upper()))
    print(args.level)
    print(getattr(logging, args.level.upper()))

    log.info("----------------------------------------------------------------")
    log.info("---------------------------pgstorm------------------------------")
    log.info("----------------------------------------------------------------")

    test_args = {
        "test_type": args.type,
        "sql": sql,
        "connection_string": args.connection_string,
        "handler": result_handler,
        "check_value": args.value
    }

    generate_threads(args.threads, test_args, args.delay)

if __name__ == 'main':
    main()