
class Parse(object):
    def __init__(self, nlp, text, collapse_punctuation, collapse_phrases):
        self.doc = nlp(text)
        if collapse_punctuation:
            spans = []
            for word in self.doc[:-1]:
                if word.is_punct:
                    continue
                if not word.nbor(1).is_punct:
                    continue
                start = word.i
                end = word.i + 1
                while end < len(self.doc) and self.doc[end].is_punct:
                    end += 1
                span = self.doc[start: end]
                spans.append(
                    (span.start_char, span.end_char, word.tag_, word.lemma_, word.ent_type_)
                )
            for span_props in spans:
                self.doc.merge(*span_props)

        if collapse_phrases:
            for np in list(self.doc.noun_chunks):
                np.merge(np.root.tag_, np.root.lemma_, np.root.ent_type_)

    def to_json(self):
        words = [{'text': w.text, 'tag': w.tag_} for w in self.doc]
        arcs = []
        for word in self.doc:
            if word.i < word.head.i:
                arcs.append(
                    {
                        'start': word.i,
                        'end': word.head.i,
                        'label': word.dep_,
                        'text': str(word),
                        'dir': 'left'
                    })
            elif word.i > word.head.i:
                arcs.append(
                    {
                        'start': word.head.i,
                        'end': word.i,
                        'label': word.dep_,
                        'text': str(word),
                        'dir': 'right'
                    })
        return {'words': words, 'arcs': arcs}


class Entities(object):
    def __init__(self, nlp, text):
        self.doc = nlp(text)

    def to_json(self):
        return [
            {
                'start': ent.start_char,
                'end': ent.end_char,
                'type': ent.label_,
                'text': str(ent)
            } for ent in self.doc.ents
        ]

class Tokens(object):
    def __init__(self, nlp, text, include_sentences, token_filter, sentence_filter):
        self.doc = nlp(text)
        self.token_filter = token_filter
        self.sentence_filter = sentence_filter
        self.inc_sents = include_sentences

    def to_json(self):
        if self.inc_sents:
            return [ self.sent_to_dict(sent) for sent in self.doc.sents]
        else:
            return [ self.token_to_dict(tok) for tok in self.doc ]

    def sent_to_dict(self, sent):
        all = len(self.sentence_filter) == 0
        attrs = {
            'start': sent.start_char,
            'end': sent.end_char
        }
        if all or 'text' in self.sentence_filter:
            attrs['text'] = sent.text
        if all or 'tokens' in self.sentence_filter:
            attrs['tokens'] = [ self.token_to_dict(tok) for tok in sent ]
        return attrs

    def token_to_dict(self, tok):
        all = len(self.token_filter) == 0
        attrs = {
            'start': tok.idx,
            'end': tok.idx + len(tok),
        }
        if all or 'text' in self.token_filter:
            attrs['text'] = tok.text
        if all or 'orth' in self.token_filter:
            attrs['orth'] = tok.orth_
        if all or 'lemma' in self.token_filter:
            attrs['lemma'] = tok.lemma_
        if all or 'pos' in self.token_filter:
            attrs['pos'] = tok.pos_
        if all or 'tag' in self.token_filter:
            attrs['tag'] = tok.tag_
        if all or 'dep' in self.token_filter:
            attrs['dep'] = tok.dep_
        # if all or 'vector' in self.token_filter:
        #     attrs['vector'] = tok.vector.tolist()
        if all or 'ent_type' in self.token_filter:
            attrs['ent_type'] = tok.ent_type_
        if all or 'ent_iob_' in self.token_filter:
            attrs['ent_iob'] = tok.ent_iob_
        if all or 'norm' in self.token_filter:
            attrs['norm'] = tok.norm_
        if all or 'lower' in self.token_filter:
            attrs['lower'] = tok.lower_
        if all or 'shape' in self.token_filter:
            attrs['shape'] = tok.shape_
        if all or 'prefix' in self.token_filter:
            attrs['prefix'] = tok.prefix_
        if all or 'suffix' in self.token_filter:
            attrs['suffix'] = tok.suffix_
        if all or 'is_alpha' in self.token_filter:
            attrs['is_alpha'] = tok.is_alpha
        if all or 'is_ascii' in self.token_filter:
            attrs['is_ascii'] = tok.is_ascii
        if all or 'is_digit' in self.token_filter:
            attrs['is_digit'] = tok.is_digit
        if all or 'is_lower' in self.token_filter:
            attrs['is_lower'] = tok.is_lower
        if all or 'is_upper' in self.token_filter:
            attrs['is_upper'] = tok.is_upper
        if all or 'is_title' in self.token_filter:
            attrs['is_title'] = tok.is_title
        if all or 'is_punct' in self.token_filter:
            attrs['is_punct'] = tok.is_punct
        if all or 'is_left_punct' in self.token_filter:
            attrs['is_left_punct'] = tok.is_left_punct
        if all or 'is_right_punct' in self.token_filter:
            attrs['is_right_punct'] = tok.is_right_punct
        if all or 'is_space' in self.token_filter:
            attrs['is_space'] = tok.is_space
        if all or 'is_bracket' in self.token_filter:
            attrs['is_bracket'] = tok.is_bracket
        if all or 'is_quote' in self.token_filter:
            attrs['is_quote'] = tok.is_quote
        if all or 'is_currency' in self.token_filter:
            attrs['is_currency'] = tok.is_currency
        if all or 'like_url' in self.token_filter:
            attrs['like_url'] = tok.like_url
        if all or 'like_num' in self.token_filter:
            attrs['like_num'] = tok.like_num
        if all or 'like_email' in self.token_filter:
            attrs['like_email'] = tok.like_email
        if all or 'is_oov' in self.token_filter:
            attrs['is_oov'] = tok.is_oov
        if all or 'is_stop' in self.token_filter:
            attrs['is_stop'] = tok.is_stop
        if all or 'cluster' in self.token_filter:
            attrs['cluster'] = tok.cluster
        return attrs

class Sentences(object):
    def __init__(self, nlp, text):
        self.doc = nlp(text)

    def to_json(self):
        sents = [sent.string.strip() for sent in self.doc.sents]
        return sents
