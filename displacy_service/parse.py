class Parse:
    def __init__(self, nlp, text, collapse_punctuation, collapse_phrases):
        self.doc = nlp(text)

        with self.doc.retokenize() as retokenizer:
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
                    spans.append((start, end, word.tag_, word.lemma_, word.ent_type_))
                for start, end, tag, lemma, ent in spans:
                    retokenizer.merge(
                        self.doc[start:end],
                        attrs={"LEMMA": lemma, "TAG": ent, "POS": tag},
                    )

            if collapse_phrases:
                for np in list(self.doc.noun_chunks):
                    retokenizer.merge(
                        self.doc[np.start : np.end],
                        attrs={
                            "LEMMA": np.lemma_,
                            "TAG": np.root.tag_,
                            "POS": np.root.tag_,
                        },
                    )

    def to_json(self):
        words = [{"text": w.text, "tag": w.tag_} for w in self.doc]
        arcs = []
        for word in self.doc:
            if word.i < word.head.i:
                arcs.append(
                    {
                        "start": word.i,
                        "end": word.head.i,
                        "label": word.dep_,
                        "text": str(word),
                        "dir": "left",
                    }
                )
            elif word.i > word.head.i:
                arcs.append(
                    {
                        "start": word.head.i,
                        "end": word.i,
                        "label": word.dep_,
                        "text": str(word),
                        "dir": "right",
                    }
                )
        return {"words": words, "arcs": arcs}


class Entities:
    def __init__(self, nlp, text):
        self.doc = nlp(text)

    def to_json(self):
        return [
            {
                "start": ent.start_char,
                "end": ent.end_char,
                "type": ent.label_,
                "text": str(ent),
            }
            for ent in self.doc.ents
        ]


class Sentences:
    def __init__(self, nlp, text):
        self.doc = nlp(text)

    def to_json(self):
        sents = [sent.text.strip() for sent in self.doc.sents]
        return sents


class SentencesDependencies(Parse):
    def to_json(self):
        sents = []
        for sent in self.doc.sents:
            words = [{"text": w.text, "tag": w.tag_} for w in sent]
            arcs = []
            for word in sent:
                if word.i < word.head.i:
                    arcs.append(
                        {
                            "start": word.i,
                            "end": word.head.i,
                            "label": word.dep_,
                            "text": str(word),
                            "dir": "left",
                        }
                    )
                elif word.i > word.head.i:
                    arcs.append(
                        {
                            "start": word.head.i,
                            "end": word.i,
                            "label": word.dep_,
                            "text": str(word),
                            "dir": "right",
                        }
                    )

            sents.append(
                {
                    "sentence": sent.text.strip(),
                    "dep_parse": {"words": words, "arcs": arcs},
                }
            )
        return sents
