from wsgiref import simple_server

from displacy_service.server import APP


def run():
    httpd = simple_server.make_server('0.0.0.0', 8000, APP)
    httpd.serve_forever()
