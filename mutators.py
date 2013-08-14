#!/usr/bin/env python
#-*- coding:utf-8 -*-

# MutProxy - set of different mutators
# Michal Melewski <michal.melewski@gmail.com>

import re
import itertools

MATCH_RESPONSE=1
MATCH_REQUEST=2

class MutatorFrame:
    match=""
    
    def __init__(self, match):
        raise NotImplementedError
    
    def set_match(self,match):
        self.match = match
    
    def check_match(self,req):
        if self.match != "":
            m=re.search(self.match,req)
            if m and m.group(0):
                return True
            else:
                return False
        else:
            return True
    
    def mutate(self, data=""):
        return date

class SimpleMutator(MutatorFrame):
    payload=[]
    gen = None
    
    def __init__(self):
        pass
    
    def add_payload(self,payload):
        self.payload.append(payload)
        self.gen = itertools.cycle(self.payload)
    
    def mutate(self, data=""):
            return self.gen.next()

class SwapMutator(MutatorFrame):
    def __init__(self):
        pass
        
    def mutate(self, data=""):
        return data.swapcase()

class OverflowMutator(MutatorFrame):
    mul = 128
    
    def __init__(self):
        pass

    def mutate(self, data=""):
        self.mul*=2
        return "A"*self.mul

class ReverseMutator(MutatorFrame):
    def __init__(self):
        pass

    def mutate(self, data=""):
        d = data.strip()
        return d[::-1]+"\n"
