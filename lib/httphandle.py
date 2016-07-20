#coding=utf-8

class HttpHandle:
    '''
    handle http request.
    '''
    def __init__(self, request=''):
        self.request = request

    def get_method(self):
        return str(self.request.split(' ')[0])

    def get_path(self):
        return str(self.request.split(' ')[1])

    def get_version(self):
        return str(self.request.split('\r\n')[0].split(' ')[2])

    def get_headers(self):
        headers = {}
        for one in self.request.split('\r\n\r\n')[0].split('\r\n')[1:]:
            key = one.split(':')[0].lstrip()
            value = one.split(':', 1)[1].lstrip()
            headers[key] = value
        return headers

    def get_body(self):
        return str(self.request.split('\r\n\r\n', 1)[1])
