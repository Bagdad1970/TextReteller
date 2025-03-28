from src.Entity import Entity
from src.EntityDict import EntityDict


class SimpleEntityFinder:
    def __init__(self, parsed_text):
        self.parsed_text = parsed_text

    def find_entities(self) -> EntityDict:
        """
        Finds simple entities in text.
        :return: Instance of EntityDict, that stores simple text entities
        """
        entity_dict = EntityDict()
        # найдем root (сказуемое)
        # то слово типа nsubj, obj, ... которое с ним связано через head_id явл. подлежащим
        # после этого также проверяется к какой части речи принадлежит слово
        for sent_index, sentence in enumerate(self.parsed_text.sents):
            for word_index, word in enumerate(sentence.tokens):
                if word.pos == 'NOUN':
                    # продолжаем читать слова, пока не закончится flat::... т.к. может быть именованой сущностью
                    entity = Entity(name=word.text)
                    entity.add_index(sent_index, word_index)
                    entity.add_relation(word.rel)

                    entity_dict.add_entity(entity)

        return entity_dict