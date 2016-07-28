import importlib
import os
from urlparse import urlparse

def scan(script, target_ip, target_port, productname={}):
    result = []

    for ones in script:
        if os.path.isdir('script/' + ones):
            for onef in os.listdir('script/' + ones):
                if '.py' in onef and '.pyc' not in onef and 't.py' != onef and '__init__.py' != onef:
                    print '[*] script.' + ones + '.' + onef[:-3], 'testing...',
                    mod = importlib.import_module('script.' + ones + '.' + onef[:-3])
                    if target_port != '':
                        result.append(mod.P().verify(ip=target_ip, port=target_port, productname=productname))
                    else:
                        result.append(mod.P().verify(ip=target_ip, productname=productname))
                    if result[-1]['result'] == True:
                        print '[!]'
                    else:
                        print
        else:
            if '.py' in onef and '.pyc' not in onef and 't.py' != onef and '__init__.py' != onef:
                ones = ones.replace('/', '.')
                print '[*] script.' + ones[:-3], 'testing...',
                mod = importlib.import_module('script.' + ones[:-3])
                if target_port != '':
                    result.append(mod.P().verify(ip=target_ip, port=target_port, productname=productname))
                else:
                    result.append(mod.P().verify(ip=target_ip, productname=productname))
                if result[-1]['result'] == True:
                    print '[!]'
                else:
                    print
    return result

def out(output, result):
    wresult = '======================= pocmap v1.0 =======================\n'
    for oner in result:
        if oner['result'] == True:
            for k, v in oner['VerifyInfo'].iteritems():
                wresult += '{k}: {v}\n'.format(k=k, v=v)
            wresult += '-----------------------------------------------------------\n'
    f = open(output, 'w')
    f.write(wresult)
    f.close()
    return

def handle_url(url):
    url = urlparse(url)
    if ':' in url.netloc:
        target_ip = str(url.netloc.split(':')[0])
        target_port = str(url.netloc.split(':')[1])
    else:
        target_ip = str(url.netloc)
        if str(url.scheme) == 'https':
            target_port = '443'
        else:
            target_port = '80'
    path = url.path
    return target_ip, target_port, path

def handle_target(target):
    target_ip = ''
    target_port = ''
    if ':' in target:
        target_ip = target.split(':')[0]
        target_port = target.split(':')[1]
    else:
        target_ip = target
    return target_ip, target_port
