#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import asyncore
import socket
import time
import getopt

from logger import *
from config import setup

BUFFER_SIZE = 8192

MATCH_RESPONSE=1
MATCH_REQUEST=2

        
class EndpointSocket(asyncore.dispatcher):
    destination = None
    active_injector=0
    injectors_req=[]
    injectors_rsp=[]
    
    def __init__(self, conn=None):
        self._outbuf = []
        asyncore.dispatcher.__init__(self, conn)
        self.logger = Logger(str(int(time.time()))) #TODO(carstein): come up with better name
             
    def set_dst(self, dst):
        """Set the destination for a socket"""
        self.destination = dst
        
    def write(self, data):
        """Write data to the socket"""
        if data:
            self._outbuf.append(data)
            self.logger.log("Send: %s\n"%data.strip())
            self.handle_write()    
            
    def register_injector(self,injector, endpoint):
        """Register injector class to modify traffic"""
        if endpoint == MATCH_REQUEST:
            self.injectors_req.append(injector)
        elif endpoint == MATCH_RESPONSE:
            self.injectors_rsp.append(injector)
        else:
            return False
            
   ##### Handle events #####   
    def handle_read(self):
        data = self.recv(BUFFER_SIZE)
        if data:
            self.logger.log("Read: %s\n"%data.strip())
            
            if self.active_injector: 
                # injection takes place here
                data=self.active_injector.inject()
                self.active_injector=None
                
            for inj in self.injectors_rsp:
                if inj.check_match(data):
                    data = inj.inject(data)
            
            self.destination.write(data)

    def handle_write(self):
        buf = self._outbuf
        while buf:
            data = buf.pop(0)
            if data:
                #injector logic
                for inj in self.injectors_req:
                    if inj.check_match(data):
                        self.active_injector=inj
                
                sent = self.send(data)
                if sent < len(data):
                    buf.insert(0, data[sent:])
                    break
                
    def handle_connect(self):
        self.destination.write('')
       
    def handle_close (self):
        print "Closing endpoint socket"
        self.destination.close()
        self.destination = None
        self.logger.close()
        self.close()

class ProxyServer(asyncore.dispatcher):
    dst=None
    
    def __init__(self, lsthost, lstport, dsthost, dstport):
        self.dst = (dsthost, dstport)
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((lsthost, lstport))
        self.listen(5)
        
        print "Proxy server (%s:%s) -> (%s:%s) initialized"%(lsthost,lstport,dsthost,dstport)

    def handle_accept(self):
        """Handle new connection through proxy - create two endpoints and pass traffic to them"""         
        pair = self.accept()

        if pair is None:
            pass
        else:
            conn, addr = pair
            conn.setblocking(0)
            
            print "Accepting connection from %s"%str(addr)
            
            # Create endpoint sockets
            ep1 = EndpointSocket() #Socket from client to proxy
            ep2 = EndpointSocket() #Socket from proxy to final destination
            
            # Set destinations
            ep1.set_dst(ep2)
            ep2.set_dst(ep1)

            # Register injectors
            for entry in setup:
                injector = entry["injector"]
                if entry.haskey("match"): injector.set_match(entry["match"])

                ep2.register_injector(injector, entry.endpoint)

            # Fire up proxy
            ep2.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            ep1.set_socket(conn)
            ep1.connected = 1
            ep2.connect(self.dst)
            
            
def print_help():
    print(
    """Usage: ./proxy.py -l lhost:lport  -d dhost:dport -i injector [-h] 
    -h                  - print this help 
    -l lhost:lport      - listen on this host and port
    -d dsthost:dport    - destination host and port"""
    )
    sys.exit(0)


def main():

    short_options = "hl:d:"
    long_options = ['help','listen=','destination=']

    try:
        opt,args=getopt.getopt(sys.argv[1:],short_options,long_options)
    except:
        print_help()

    for o, ext in opt:
        if o in ("-h","--help"):
            print_help()
        if o in ("-l","--listen"):
            lhost,lport = ext.split(":")
        if o in ("-d","--destination"):
            dhost,dport = ext.split(":")
 
    server = ProxyServer(lhost, int(lport), dhost, int(dport))
    
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print('Proxy closed.\n')
        return 0
    
if __name__ == "__main__":
    sys.exit(main())
