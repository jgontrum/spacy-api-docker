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
parser.add_argument('text', type=str, location='json')
parser.add_argument('texts', type=list, location='json')
parser.add_argument('fields', type=list, default=[], location='json')


class Spacy(Resource):

    def get(self):
        return 200

    def post(self):
        t0 = time.time()
        args = parser.parse_args()

        validation = self.__validate_input(args)
        if validation:
            return validation, 500

        ret = {
            'version': '1.1.2',
            'lang': language
        }

        if args.get('text'):
            # Analyze only a single text
            ret.update(
                self.__analyze(args.get('text'), args.get('fields')))
        elif args.get('texts'):
            ret['texts'] = [
                self.__analyze(text, args.get('fields'))
                for text in args.get('texts')]
            ret['numOfTexts'] = len(args.get('texts'))

        ret['performance'] = time.time() - t0,
        ret['error'] = False
        return ret, 200

    @staticmethod
    def __validate_input(args: dict):
        message = ""
        if not args.get('text') and not args.get('texts'):
            message = "No text(s) received."
        if args.get('texts') and not isinstance(args.get('texts'), list):
            message = 'Wrong format for "texts". A list of strings is required.',
        if message:
            return {
               'message': message,
               'error': True
           }
        return None

    @staticmethod
    def __analyze(text: str, fields: list):
        doc = nlp(text)

        ret = {
            'numOfSentences': len(list(doc.sents)),
            'numOfTokens': len(list(doc)),
            'sentences': []
        }

        for sentence in doc.sents:
            sentence_analysis = [{
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
            } for w in sentence]

            if fields:
                # Remove certain fields if requested
                sentence_analysis = [
                    dict([(k, v) for k, v in token.items() if k in fields])
                    for token in sentence_analysis
                ]
            ret['sentences'].append(sentence_analysis)
        return ret

api.add_resource(Spacy, '/api')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.environ.get('PORT') or 5000)
