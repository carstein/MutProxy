#!/usr/bin/env python
#-*- coding:utf-8 -*-

# MutProxy - set of different loggers
# Michal Melewski <michal.melewski@gmail.com>

import time

class TextLogger:
    def setup(self, log_name=""):
        self.log_file = open(log_name,"w+")
        self.log_file.write("Starting text logger\n")

    def log(self, data, direction=""):
        self.log_file.write(" ".join([str(int(time.time())), direction, data.strip(), "\n"]))

    def close(self):
        self.log_file.close()

class BinaryLogger:
    def setup(self, log_name=""):
        self.log_file = open(log_name,"w+")
        self.log_file.write("Starting binary logger\n")

    def log(self, data, direction=""):
        self.log_file.write(" ".join([str(int(time.time())), direction, data.encode("hex"), "\n"]))

    def close(self):
        self.log_file.close()
