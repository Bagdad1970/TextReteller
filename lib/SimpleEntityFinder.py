from lib.Entity import Entity
from EntityDict import EntityDict
from natasha import (
    Doc,
    Segmenter,
    NewsEmbedding,
    NewsSyntaxParser
)

segmenter = Segmenter()
embedding = NewsEmbedding()
syntax_parser = NewsSyntaxParser(embedding)

class SimpleEntityFinder:
    def __init__(self, text):
        self.text = text

    def find_entities(self) -> EntityDict:
        if self.text == "":
            return EntityDict()

        doc = Doc(self.text)
        doc.segment(segmenter)  # найти, что можно оптимизировать
        doc.parse_syntax(syntax_parser)

        entity_dict = EntityDict()
        for sentence_index, sentence in enumerate(doc.sents):
            for word_index, word in enumerate(sentence.tokens):
                if word.rel == 'nsubj':
                    # продолжаем читать слова, пока не закончится flat::... т.к. может быть именованой сущностью
                    entity = Entity(name=word.text)
                    entity.add_index(sentence_index=sentence_index, word_index=word_index)
                    entity_dict.add_entity(entity)

        return entity_dict