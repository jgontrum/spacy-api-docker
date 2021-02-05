from fastapi import APIRouter

from .shared import nlp
from ..models.nlp import Sentence, Token, TextAnalysis, SpacyResponse
from ..models.request import SpacyRequest

router = APIRouter()


@router.post("/", response_model=SpacyResponse)
def run_spacy(request: SpacyRequest) -> SpacyResponse:
    ret = []
    for text in request.texts:
        parsed = nlp(text)
        sentences = []
        for sentence in parsed.sents:
            sentences.append(
                Sentence(
                    sentence=str(sentence),
                    tokens=[
                        Token(
                            text=t.text,
                            token=t.norm_,
                            lemma=t.lemma_,
                            pos=t.pos_,
                            ner=t.ent_type_,
                            is_stop_word=t.is_stop,
                            character_offset=t.idx,
                            length=len(t.text),
                            offset=t.i,
                            morphology=t.morph.to_dict(),
                        )
                        for t in sentence
                    ],
                    num_tokens=len(sentence),
                )
            )

        ret.append(
            TextAnalysis(text=text, sentences=sentences, num_sentences=len(sentences))
        )

    return SpacyResponse(texts=ret, num_texts=len(ret))
