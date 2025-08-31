from re import IGNORECASE, findall

import nltk
import spacy
from nltk.corpus import stopwords
from structlog.stdlib import BoundLogger, get_logger
from unidecode import unidecode

logger: BoundLogger = get_logger()

nltk.download("stopwords")


class NLP:
    @staticmethod
    def process(content: str) -> list[str]:
        content = unidecode(content)
        content = " ".join(findall(r"[a-z]+", content, IGNORECASE))

        nlp = spacy.load("en_core_web_sm")

        # Tokenização + Lematização com Spacy
        doc = nlp(content)
        return [
            token.lemma_
            for token in doc
            if token.text.lower() not in stopwords.words("portuguese")
        ]
