#coding=utf-8

import socket
import sys
import getopt
import os
import importlib
import threading
import json
import random
from lib.database import Database
from lib.httphandle import HttpHandle
from lib.api import handle_url, scan, handle_target

adminid = 'superfish'
bind_ip = '127.0.0.1'
bind_port = 8776
threads = []
delete = {}

def t_scan(opt, target_ip, target_port, productname, taskid, db):
    db.execute("insert into data(taskid, status) values('{taskid}', 'running');".format(taskid=taskid))
    db.commit()
    result = scan(opt['script'], target_ip, target_port, productname)
    db.execute("update data set status='terminal', vuls='{result}' where taskid={taskid};".format(result=str(result), taskid=taskid))
    db.commit()
    return

def scan_new(headers, body, connection, db):
    global delete
    respheader = 'HTTP/1.1 200 OK\r\nServer: pocmapapi/scan_new\r\n\r\n'
    target_ip = ''
    target_port = ''
    productname = {}
    respbody = {}

    result = []
    respbody['state'] = 'fail'
    opt = json.loads(body)
    if opt.has_key('url') and opt.has_key('web'):
        target_ip, target_port, productname['path'] = handle_url(opt['url'])
        if opt.has_key('cookie'):
            productname['cookie'] = opt['cookie']
    elif opt.has_key('target'):
        target = opt['target']
        target_ip, target_port = handle_target(target)
    else:
        connection.send(respheader + str(respbody))
        return
    if opt.has_key('script') and opt['script'] != []:
        taskid = str(random.randint(1000000000, 9999999999))
        respbody['taskid'] = taskid
        respbody['state'] = 'success'
        t = threading.Thread(target=t_scan, args=(opt, target_ip, target_port, productname, taskid, db))
        t.setDaemon(True)
        t.start()
        connection.send(respheader + str(respbody))
    else:
        connection.send(respheader + str(respbody))

    delete[taskid] = False
    while True:
        if not t.isAlive() or delete[taskid]:
            break
    return

def scan_delete(headers, body, connection, db):
    global delete
    respheader = 'HTTP/1.1 200 OK\r\nServer: pocmapapi/scan_delete\r\n\r\n'
    respbody = {}

    respbody['state'] = 'fail'
    if headers.has_key('Taskid'):
        taskid = headers['Taskid']
        delete[taskid] = True
        db.execute("delete from data where taskid={};".format(taskid=taskid))
        db.commit()
        respbody['state'] = 'success'
        connection.send(respheader + str(respbody))
    else:
        connection.send(respheader + str(respbody))
    return

def scan_data(headers, body, connection, db):
    return

def admin_list(headers, body, connection, db):
    return


def handle_client(connection, db):
    switch = {'/scan/new':scan_new,
              '/scan/delete':scan_delete,
              '/scan/data':scan_data,
              '/admin/list':admin_list}
    
    try:
        connection.settimeout(5)
        buf = connection.recv(1024)
        req = HttpHandle(buf)
        path = req.get_path()
        headers = req.get_headers()
        body = req.get_body()
        if switch.has_key(path):
            switch[path](headers, body, connection, db)
    except socket.timeout:
        pass
    finally:
        connection.close()
    return

def server_loop():
    global bind_ip
    global bind_port
    global threads

    db = Database()
    db.connect()
    db.init()
    db.commit()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((bind_ip, bind_port))
    s.listen(20)
    while True:
        connection, address = s.accept()
        t = threading.Thread(target=handle_client, args=(connection, db))
        threads.append(t)
        t.setDaemon(True)
        t.start()
    db.disconnect()
    return




