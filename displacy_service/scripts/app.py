import os
from wsgiref import simple_server

import falcon
from spacy.symbols import ORTH

from displacy_service.server import DepResource, EntResource, SentsResources, SentsDepResources, SchemaResource, \
    ModelsResource, VersionResource
from displacy_service.server import MODELS, get_model

app = application = falcon.App()

app.add_route('/dep', DepResource())
app.add_route('/ent', EntResource())
app.add_route('/sents', SentsResources())
app.add_route('/sents_dep', SentsDepResources())
app.add_route('/{model_name}/schema', SchemaResource())
app.add_route('/models', ModelsResource())
app.add_route('/version', VersionResource())


def run():
    for model in MODELS:
        print("Load model ", model)
        loaded_model = get_model(model)
        special_cases_str = os.getenv(f"{model}_special_cases", "")
        if special_cases_str:
            for special_case in special_cases_str.split(','):
                loaded_model.tokenizer.add_special_case(
                    special_case,
                    [{ORTH: special_case}]
                )

    print("Loaded all models. Starting HTTP server.")
    httpd = simple_server.make_server('0.0.0.0', 8000, app)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
