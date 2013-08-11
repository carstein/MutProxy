#!/usr/bin/env python
#-*- coding:utf-8 -*-

class Logger:
    def __init__(self,log_name):
        self.log_file = open(log_name,"w+")
        self.log("Starting connection logging\n")
        
    def log(self,text):
        self.log_file.write(text+"\n")
        
    def close(self):
        self.log_file.close()
