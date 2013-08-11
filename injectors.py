#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
import itertools

MATCH_RESPONSE=1
MATCH_REQUEST=2

class InjectorFrame:
    match=""
    
    def __init__(self, match):
        raise NotImplementedError
    
    def set_match(self,match):
        self.match = match
    
    def check_match(self,req):
        if match != "":
            m=re.search(self.match,req)
            if m and m.group(0):
                return True
            else:
                return False
        else:
            return True
    
    def inject(self, data=""):
        return date
        
class SimpleInjector(InjectorFrame):
    payload=[]
    gen = None
    
    def __init__(self):
        pass
    
    def add_payload(self,payload):
        self.payload.append(payload)
        self.gen = itertools.cycle(self.payload)
    
    def inject(self, data=""):
            return self.gen.next()

class SwapInjector(InjectorFrame):
    def __init__(self):
        pass
        
    def inject(self, data=""):
        return data.swapcase()

class OverflowInjector(InjectorFrame):
    mul = 128
    
    def __init__(self):
        pass

    def inject(self, data=""):
        self.mul*=2
        return "A"*self.mul
