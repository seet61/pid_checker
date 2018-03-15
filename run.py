#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, sys

import logging, schedule
from logging.handlers import RotatingFileHandler
import time

from service import find_syslog, Service
from subprocess import Popen

pid_file = '/var/tmp/pid'
script = '/usr/bin/pix'

class MyService(Service):
    def __init__(self, *args, **kwargs):
        super(MyService, self).__init__(*args, **kwargs)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        rfh = RotatingFileHandler('logger.log', mode='a', maxBytes=1024, backupCount=10, encoding='utf8', delay=0)
        rfh.setFormatter(formatter)
        self.logger.addHandler(rfh)
        self.logger.setLevel(logging.INFO)

    def read_pid(self):
        with open(pid_file, 'r') as data:
            for line in data:
                return line

    def main(self):
        pid = self.read_pid()
        self.logger.info("pid: " + pid)
        if (os.path.exists("/proc/"+pid) == False):
            self.logger.info('start service')
            p = Popen(script, shell=True)
            p.communicate()

    def run(self):
        self.logger.info('#'*80)
        self.logger.info('starting')
        schedule.every(1).minutes.do(self.main)
        while not self.got_sigterm():
            schedule.run_pending()
        self.logger.info('stoped')

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        sys.exit('Syntax: %s COMMAND' % sys.argv[0])

    cmd = sys.argv[1].lower()
    service = MyService('my_service', pid_dir='/tmp')

    if cmd == 'start':
        service.start()
    elif cmd == 'stop':
        service.stop()
    elif cmd == 'status':
        if service.is_running():
            print "Service is running."
        else:
            print "Service is not running."
    else:
        sys.exit('Unknown command "%s".' % cmd)