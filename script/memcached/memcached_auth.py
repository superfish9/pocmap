#!/usr/bin/env python
# encoding: utf-8
from t import T
import socket
import requests,urllib2,json,urlparse
class P(T):
    def __init__(self):
        T.__init__(self)
    def verify(self,head='',context='',ip='',port='11211',productname={},keywords='',hackinfo=''):

        result = {}
        result['result']=False
        r=None
        payload = '\x73\x74\x61\x74\x73\x0a'  # command:stats
        s = socket.socket()
        socket.setdefaulttimeout(10)
        try:
            s.connect((ip, int(port)))
            s.send(payload)
            recvdata = s.recv(2048)  # response larger than 1024
    
        if recvdata and 'STAT version' in recvdata:
            result['result']=True
            result['VerifyInfo'] = {}
            result['VerifyInfo']['type']='Memcached unauth'
            result['VerifyInfo']['URL'] =ip+':'+port
            result['VerifyInfo']['payload']='None'
            result['VerifyInfo']['result'] ='Memcached unauth'

        except Exception,e:
            print e.text
        finally:
            s.close()
            return result
if __name__ == '__main__':
    print P().verify(ip='140.114.108.4',port='80')