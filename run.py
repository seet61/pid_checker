#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, sys

import logging, schedule
from logging.handlers import RotatingFileHandler
import time

from service import find_syslog, Service
from subprocess import Popen

pid_file = '/root/.bitcoinz/zcashd.pid'
script = '/root/bitcoinz/src/zcashd'
script_service = 'service znomp restart'

def read_pid():
    with open(pid_file, 'r') as data:
        for line in data:
            return line[:-1]

def main():
    pid = read_pid()
    logging.basicConfig(filename=os.getcwd() +'checker.log', level=DEBUG, format='%(asctime)-15s %(levelname)s %(message)s')
    logging.info("start")
    if (os.path.exists("/proc/"+pid) == False):
        logging.info('start service')
        p = Popen(script, shell=True)
        p.communicate()
        p = Popen(script_service, shell=True)
        p.communicate()
    logging.info("stop")        

if __name__ == '__main__':
    main()