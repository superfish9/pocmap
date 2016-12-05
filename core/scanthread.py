import threading
import sys
sys.path.append("..")
from lib.api import handle_url, scan, handle_target

class ScanThread(threading.Thread):
    '''
    scan thread.
    '''
    def __init__(self, result, que, is_web, script, lock):
        threading.Thread.__init__(self)
        self.daemon = False
        self.result = result
        self.queue = que
        self.is_web = is_web
        self.script = script
        self.lock = lock

    def run(self):
        target_ip = ''
        target_port = ''
        productname = {}
        s_result = []
        
        while True:
            if self.queue.empty():
                break
            item = self.queue.get()
            if self.is_web:
                target_ip, target_port, productname['path'] = handle_url(item)
            else:
                target_ip, target_port = handle_target(item)
            print '[**] test', target_ip
            s_result = scan(self.script, target_ip, target_port, productname)
            self.lock.acquire()
            self.result += s_result
            self.lock.release()
        return

