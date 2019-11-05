from spacy.symbols import ORTH

contractions = [[{ORTH: "you've"}],	[{ORTH: "you're"}],	[{ORTH: "you'll"}],	[{ORTH: "you'd"}],
                [{ORTH: "y'all'd've"}],	[{ORTH: "y'all"}],	[{ORTH: "wouldn't"}], [{ORTH: "would've"}],
                [{ORTH: "won't"}], [{ORTH: "why's"}],	[{ORTH: "why're"}],	[{ORTH: "why'd"}], [{ORTH: "whom'st'd've"}],
                [{ORTH: "whom'st"}], [{ORTH: "who've"}], [{ORTH: "who's"}], [{ORTH: "who're"}], [{ORTH: "who'll"}],
                [{ORTH: "who'd've"}], [{ORTH: "who'd"}], [{ORTH: "which's"}], [{ORTH: "where've"}],
                [{ORTH: "where's"}], [{ORTH: "where're"}], [{ORTH: "where'd"}], [{ORTH: "when's"}],
                [{ORTH: "what've"}], [{ORTH: "what's"}], [{ORTH: "what're"}], [{ORTH: "what'll"}],
                [{ORTH: "what'd"}], [{ORTH: "weren't"}], [{ORTH: "we've"}],	[{ORTH: "we're"}],	[{ORTH: "we'll"}],
                [{ORTH: "we'd've"}],[{ORTH: "we'd"}], [{ORTH: "wasn't"}], [{ORTH: "those're"}], [{ORTH: "this's"}],
                [{ORTH: "they've"}], [{ORTH: "they're"}], [{ORTH: "they'll"}], [{ORTH: "they'd"}],
                [{ORTH: "these're"}], [{ORTH: "there's"}], [{ORTH: "there're"}], [{ORTH: "there'll"}],
                [{ORTH: "there'd"}], [{ORTH: "that's"}], [{ORTH: "that're"}], [{ORTH: "that'll"}],
                [{ORTH: "that'd"}], [{ORTH: "something's"}], [{ORTH: "someone's"}], [{ORTH: "somebody's"}],
                [{ORTH: "so're"}], [{ORTH: "shouldn't've"}], [{ORTH: "shouldn't"}],	[{ORTH: "should've"}],
                [{ORTH: "she's"}], [{ORTH: "she'll"}], [{ORTH: "she'd"}], [{ORTH: "shan't"}], [{ORTH: "shalln't"}],
                [{ORTH: "oughtn't"}], [{ORTH: "ol'"}], [{ORTH: "o'er"}], [{ORTH: "o'clock"}], [{ORTH: "noun's"}],
                [{ORTH: "needn't"}], [{ORTH: "ne'er"}], [{ORTH: "mustn't've"}], [{ORTH: "mustn't"}],
                [{ORTH: "must've"}], [{ORTH: "mightn't"}], [{ORTH: "might've"}], [{ORTH: "mayn't"}],
                [{ORTH: "may've"}], [{ORTH: "ma'am"}], [{ORTH: "let's"}], [{ORTH: "it's"}], [{ORTH: "it'll"}],
                [{ORTH: "it'd"}], [{ORTH: "isn't"}], [{ORTH: "i've"}], [{ORTH: "i'm'o"}], [{ORTH: "i'm'a"}],
                [{ORTH: "i'm"}], [{ORTH: "i'll"}], [{ORTH: "i'd"}], [{ORTH: "howdy"}], [{ORTH: "how's"}],
                [{ORTH: "how're"}], [{ORTH: "how'll"}], [{ORTH: "how'd"}], [{ORTH: "he've"}], [{ORTH: "he's"}],
                [{ORTH: "he'll"}], [{ORTH: "he'd"}], [{ORTH: "haven't"}], [{ORTH: "hasn't"}], [{ORTH: "hadn't"}],
                [{ORTH: "gotta"}], [{ORTH: "gonna"}], [{ORTH: "gon't"}], [{ORTH: "giv’n"}],
                [{ORTH: "gimme"}], [{ORTH: "finna"}], [{ORTH: "everyone's"}], [{ORTH: "e'er"}], [{ORTH: "don't"}],
                [{ORTH: "doesn't"}], [{ORTH: "didn't"}], [{ORTH: "dasn't"}], [{ORTH: "daresn't"}],
                [{ORTH: "daren't"}], [{ORTH: "couldn't've"}], [{ORTH: "couldn't"}], [{ORTH: "could've"}],
                [{ORTH: "can't"}], [{ORTH: " cain't"}], [{ORTH: "aren't"}], [{ORTH: "amn't"}], [{ORTH: "ain't"}],
                [{ORTH: "'twas	"}], [{ORTH: "'tis"}], [{ORTH: "'s"}], [{ORTH: "'cause"}]]


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


class Sentences(object):
    def __init__(self, nlp, text):
        self.doc = nlp(text)

    def to_json(self):
        sents = [sent.string.strip() for sent in self.doc.sents]
        return sents


class SentencesDependencies(object):
    def __init__(self, nlp, text, collapse_punctuation, collapse_phrases, collapse_contractions):

        if collapse_contractions:
            for contraction in contractions:
                nlp.tokenizer.add_special_case(contraction[0][ORTH], contraction)

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
        sents = []
        for sent in self.doc.sents:
            words = [{'text': w.text, 'tag': w.tag_} for w in sent]
            arcs = []
            for word in sent:
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

            sents.append({'sentence': sent.string.strip(),
                          'dep_parse': {'words': words,
                                        'arcs': arcs}})
        return sents

