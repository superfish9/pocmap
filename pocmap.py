#coding=utf-8

import importlib
import sys
import getopt
import os
from urlparse import urlparse

is_web = False
result = []

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

def scan(script, target, port, productname):
    global is_web
    global result

    for ones in script:
        if os.path.isdir('script/' + ones):
            for onef in os.listdir('script/' + ones):
                if '.py' in onef and '.pyc' not in onef and 't.py' != onef and '__init__.py' != onef:
                    print '[*] script.' + ones + '.' + onef[:-3], 'testing...',
                    mod = importlib.import_module('script.' + ones + '.' + onef[:-3])
                    if is_web:
                        result.append(mod.P().verify(ip=target, port=port, productname=productname))
                    else:
                        result.append(mod.P().verify(ip=target))
                    if result[-1]['result'] == True:
                        print '[!]'
                    else:
                        print
        else:
            if '.py' in onef and '.pyc' not in onef and 't.py' != onef and '__init__.py' != onef:
                ones = ones.replace('/', '.')
                print '[*] script.' + ones[:-3], 'testing...',
                mod = importlib.import_module('script.' + ones[:-3])
                if is_web:
                    result.append(mod.P().verify(ip=target, port=port, productname=productname))
                else:
                    result.append(mod.P().verify(ip=target))
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

def usage():
    print 'pocmap!'
    print
    print 'usage:'
    print 'python pocmap.py -h ip -p port -s "script1 script2"'
    print 'python pocmap.py -u url -w'
    print 'python pocmap.py -f url_list.txt -o output.txt'
    print
    print 'options:'
    print '-w --web                              - is web vul, make url valid'
    print '-c --cookie=cookie                    - cookie for some web vul'
    print '-u --url=url                          - url'
    print '-t --target=ip/domain                 - ip or domain'
    print '-p --port=port                        - port, default usually for not web vul'
    print '-s --script=script                    - specify a script, none for all'
    print '-f --file=url_list.txt                - url list'   
    print '-o --output=output.txt                - file for output, default is output.txt'
    print '-h --help                             - usage'
    print
    print 'tip: if the target service is default, there is no need for "-w" or "--web".'
    sys.exit(0)

def main():
    global is_web
    global result

    url_list = ''
    target = ''
    port = ''
    url = ''
    productname = {}
    script = []
    output = 'output.txt'

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'wc:u:t:p:s:f:o:h', ['web', 'cookie', 'url', 'target', 'port', 'script', 'file', 'output', 'help'])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o ,a in opts:
        if o in ('-h', '--help'):
            usage()
        elif o in ('-o', '--output'):
            output = str(a).strip()
        elif o in ('-f', '--file'):
            url_list = str(a).strip()
        elif o in ('-s', '--script'):
            script = str(a).strip().split(' ')
        elif o in ('-p', '--port'):
            port = str(a).strip()
        elif o in ('-t' '--target'):
            target = str(a).strip()
        elif o in ('-u', '--url'):
            url = str(a).strip()
        elif o in ('-c', '--cookie'):
            productname['cookie'] = str(a).strip()
        elif o in ('-w', '--web'):
            is_web = True
        else:
            assert False, "Unhandled Option"

    if script == []:
        for one in os.listdir('script'):
            if '__init__.py' != one:
                script.append(str(one))

    print '[***] start.'
    if url_list != '':
        f = open(url_list, 'r')
        urllist = f.readlines()
        f.close()
        for oneu in urllist:
            if oneu == '\n':
                continue
            target, port, productname['path'] = handle_url(oneu[:-1])
            print '[**] test', target
            scan(script, target, port, productname)
    elif url != '':
        target, port, productname['path'] = handle_url(url)
        print '[**] test', target
        scan(script, target, port, productname)
    else:
        print '[**] test', target
        scan(script, target, port, productname)

    out(output)
    print '[***] done.'
    return

if __name__ == '__main__':
    main()


            
                




