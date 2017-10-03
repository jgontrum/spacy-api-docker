from wsgiref import simple_server

from displacy_service.server import APP, MODELS, get_model


def run():
    for model in MODELS:
      print("Load model ", model)
      get_model(model)

    print("Loaded all models. Starting HTTP server.")
    httpd = simple_server.make_server('0.0.0.0', 8000, APP)
    httpd.serve_forever()
