#coding=utf-8

import os
import sys
import getopt
from lib.api import handle_url, scan, out, handle_target

def usage():
    print 'pocmap!'
    print
    print 'usage:'
    print 'python pocmap.py -t ip:port -s "script1 script2"'
    print 'python pocmap.py -u url -w'
    print 'python pocmap.py -f target_list.txt'
    print 'python pocmap.py -f url_list.txt -w -o output.txt'
    print
    print 'options:'
    print '-w --web                              - is web vul, make url and url_list valid'
    print '-c --cookie=cookie                    - cookie for some web vul'
    print '-u --url=url                          - url'
    print '-t --target=ip/domain:port            - ip or domain : port or default'
    print '-s --script=script                    - specify a script, none for all'
    print '-f --file=ut_list.txt                 - web means url_list, or target_list'   
    print '-o --output=output.txt                - file for output, default is output.txt'
    print '-h --help                             - usage'
    print
    sys.exit(0)

def main():
    is_web = False
    ut_list = ''
    target = ''
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
            ut_list = str(a).strip()
        elif o in ('-s', '--script'):
            script = str(a).strip().split(' ')
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

    result = []
    print '[***] start.'
    if ut_list != '':
        if is_web:
            url_list = ut_list
            f = open(url_list, 'r')
            urllist = f.readlines()
            f.close()
            for oneu in urllist:
                if oneu == '\n':
                    continue
                target_ip, target_port, productname['path'] = handle_url(oneu[:-1])
                print '[**] test', target_ip
                result += scan(script, target_ip, target_port, productname)
        else:
            target_list = ut_list
            f = open(target_list, 'r')
            targetlist = f.readlines()
            f.close()
            for onet in targetlist:
                if onet == '\n':
                    continue
                target_ip, target_port = handle_target(onet[:-1])
                print '[**] test', target_ip
                result += scan(script, target_ip, target_port)
    elif url != '' and is_web:
        target_ip, target_port, productname['path'] = handle_url(url)
        print '[**] test', target_ip
        result = scan(script, target_ip, target_port, productname)
    else:
        if target == '':
            print '[^] please use -t, or use -w and -u.'
            sys.exit(1)
        target_ip, target_port = handle_target(target)
        print '[**] test', target_ip
        result = scan(script, target_ip, target_port)

    print '[***] done.'
    out(output, result)
    print '[****] result is in {output}.'.format(output=output)
    return

if __name__ == '__main__':
    main()


            
                




