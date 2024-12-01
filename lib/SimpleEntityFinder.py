from lib.Entity import Entity
from EntityDict import EntityDict
from pymorphy3 import MorphAnalyzer
from lib.TextParser import TextParser

morph = MorphAnalyzer()

class SimpleEntityFinder:
    def __init__(self, text):
        self.parsed_text = TextParser.get_processed_text(text)

    def find_entities(self) -> EntityDict:
        if self.parsed_text == "":
            return EntityDict()

        entity_dict = EntityDict()

        # найдем root (сказуемое)
        # то слово типа nsubj, obj, ... которое с ним связано через head_id явл. подлежащим
        # после этого также проверяется к какой части речи принадлежит слово
        for sent_index, sentence in enumerate(self.parsed_text.sents):
            self.parsed_text.sents[sent_index].syntax.print()
            for word_index, word in enumerate(sentence.tokens):
                #print(word.text, word.pos)
                if word.pos == 'NOUN' or word.pos == 'PROPN':
                    # продолжаем читать слова, пока не закончится flat::... т.к. может быть именованой сущностью
                    entity = Entity(name=morph.parse(word.text)[0].normal_form)
                    entity.add_index(sent_index, word_index)
                    entity.add_relation(word.rel)

                    entity_dict.add_entity(entity)

        return entity_dict