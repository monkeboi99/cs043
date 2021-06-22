import wsgiref.simple_server
import urllib.parse
from database import Simpledb


def application(environ, start_response):
    headers = [('Content-Type', 'text/plain; charset=utf-8')]

    path = environ['PATH_INFO']
    params = urllib.parse.parse_qs(environ['QUERY_STRING'])

    db = Simpledb('data.txt')

    if path == '/insert':
        db.insert(params['key'][0], params['value'][0])
        start_response('200 OK', headers)
        return ['Inserted'.encode()]
        ### YOUR CODE HERE ###
    elif path == '/select':
        s = db.select_one(params['key'][0])
        start_response('200 OK', headers)
        if s:
            return [s.encode()]
        else:
            return ['NULL'.encode()]
    elif path == '/delete':
        s = db.select_one(params['key'][0])
        start_response('200 OK', headers)
        if s:
            db.delete(params['key'][0])
            return ['deleted'.encode()]
        else:
            return ['NULL'.encode()]
        ### YOUR CODE HERE ###
    elif path == '/update':
        s = db.select_one(params['key'][0])
        start_response('200 OK', headers)
        if s:
            db.update(params['key'][0], params['value'][0])
            return ['Updated'.encode()]
        else:
            return ['NULL'.encode()]
        ### YOUR CODE HERE ###
    else:
        start_response('404 Not Found', headers)
        return ['Status 404: Resource not found'.encode()]

httpd = wsgiref.simple_server.make_server('', 8000, application)
httpd.serve_forever()