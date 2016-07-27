#coding=utf-8

import socket
import sys
import getopt
import os
import importlib
import threading
import json
from lib.database import Database
from lib.httphandle import HttpHandle

adminid = 'superfish'
bind_ip = '127.0.0.1'
bind_port = 8776
threads = []

def scan_new(headers, body):
    return

def scan_delete(headers, body):
    return

def scan_data(headers, body):
    return

def admin_list(headers, body):
    return


def handle_client(connection):
    switch = {'/scan/new':scan_new,
              '/scan/delete':scan_delete,
              '/scan/data':scan_data,
              '/admin/list':admin_list}
    
    respheader = 'HTTP/1.1 200 OK\r\nServer: pocmapapi\r\n\r\n'
    try:
        connection.settimeout(5)
        buf = connection.recv(1024)
        req = HttpHandle(buf)
        path = req.get_path()
        headers = req.get_headers()
        body = req.get_body()
        if switch.has_key(path):
            respbody = switch[path](headers, body)
        connection.send(respheader + str(respbody))
    except socket.timeout:
        pass
    finally:
        connection.close()
    return

def server_loop():
    global bind_ip
    global bind_port
    global threads

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((bind_ip, bind_port))
    s.listen(20)
    while True:
        connection, address = s.accept()
        t = threading.Thread(target=handle_client, args=(connection,))
        threads.append(t)
        t.setDaemon(True)
        t.start()
    return




