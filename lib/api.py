import importlib
import os
from urlparse import urlparse

result = []

def scan(script, target, port, productname):
    global result

    for ones in script:
        if os.path.isdir('script/' + ones):
            for onef in os.listdir('script/' + ones):
                if '.py' in onef and '.pyc' not in onef and 't.py' != onef and '__init__.py' != onef:
                    print '[*] script.' + ones + '.' + onef[:-3], 'testing...',
                    mod = importlib.import_module('script.' + ones + '.' + onef[:-3])
                    result.append(mod.P().verify(ip=target, port=port, productname=productname))
                    if result[-1]['result'] == True:
                        print '[!]'
                    else:
                        print
        else:
            if '.py' in onef and '.pyc' not in onef and 't.py' != onef and '__init__.py' != onef:
                ones = ones.replace('/', '.')
                print '[*] script.' + ones[:-3], 'testing...',
                mod = importlib.import_module('script.' + ones[:-3])
                result.append(mod.P().verify(ip=target, port=port, productname=productname))
                if result[-1]['result'] == True:
                    print '[!]'
                else:
                    print
    return

def out(output):
    global result

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
        target = str(url.netloc.split(':')[0])
        port = str(url.netloc.split(':')[1])
    else:
        target = str(url.netloc)
        if str(url.scheme) == 'https':
            port = '443'
        else:
            port = '80'
    path = url.path
    return target, port, path
