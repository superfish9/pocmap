#coding=utf-8

import sys
import getopt
from lib.api import handle_url, scan, out

def usage():
    print 'pocmap!'
    print
    print 'usage:'
    print 'python pocmap.py -h ip -p port -s "script1 script2"'
    print 'python pocmap.py -u url -w'
    print 'python pocmap.py -f url_list.txt -o output.txt'
    print
    print 'options:'
    print '-w --web                              - is web vul, make url and url_list valid'
    print '-c --cookie=cookie                    - cookie for some web vul'
    print '-u --url=url                          - url'
    print '-t --target=ip/domain                 - ip or domain'
    print '-p --port=port                        - port, default usually for not web vul'
    print '-s --script=script                    - specify a script, none for all'
    print '-f --file=url_list.txt                - url list'   
    print '-o --output=output.txt                - file for output, default is output.txt'
    print '-h --help                             - usage'
    print
    sys.exit(0)

def main():
    is_web = False
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

    result = []
    print '[***] start.'
    if url_list != '' and is_web:
        f = open(url_list, 'r')
        urllist = f.readlines()
        f.close()
        for oneu in urllist:
            if oneu == '\n':
                continue
            target, port, productname['path'] = handle_url(oneu[:-1])
            print '[**] test', target
            result = scan(script, target, port, productname)
    elif url != '' and is_web:
        target, port, productname['path'] = handle_url(url)
        print '[**] test', target
        result = scan(script, target, port, productname)
    else:
        if target == '' and port == '':
            print '[^] please use -t and -p, or use -w and -u.'
            sys.exit(1)
        print '[**] test', target
        result = scan(script, target, port)

    print '[***] done.'
    out(output, result)
    print '[****] result is in {output}.'.format(output=output)
    return

if __name__ == '__main__':
    main()


            
                




