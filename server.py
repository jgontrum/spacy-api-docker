#!/usr/bin/env python
# -*- coding: utf-8 -*-
import spacy
import os
import time
from flask import Flask
from flask_restful import reqparse, Api, Resource

language = os.environ['LANG'] or 'en'

print("Loading Language Model for '%s'..." % language)
nlp = spacy.load(language)
print("Language Model for '%s' loaded!" % language)

app = Flask("Spacy API")
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('text')


class Spacy(Resource):

    def get(self):
        return 201

    def post(self):
        t0 = time.time()
        args = parser.parse_args()
        if not args.get('text'):
            return {'message': 'Text not found!', 'error': True}, 500

        doc = nlp(args.get('text'))
        return {
            'sentences': [[
                {
                    'token': w.orth_,
                    'lemma': w.lemma_,
                    'tag': w.tag_,
                    'ner': w.ent_type_,
                    'offsets': {
                        'begin': w.idx,
                        'end': w.idx + len(w.orth_)
                    },
                    'oov': w.is_oov,
                    'stop': w.is_stop,
                    'url': w.like_url,
                    'email': w.like_email,
                    'num': w.like_num,
                    'pos': w.pos_
                } for w in sentence
            ] for sentence in doc.sents],
            'performance': time.time() - t0,
            'version': '0.101.0',
            'numOfSentences': len(list(doc.sents)),
            'numOfTokens': len(list(doc))
        }, 201

api.add_resource(Spacy, '/api')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
