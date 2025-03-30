from natasha import Doc

from src.entity import Entity
from src.entity_dict import EntityDict
from src.word_normalizer import WordNormalizer


class EntityFinder(WordNormalizer):
    def __init__(self, parsed_text: Doc):
        self.parsed_text = parsed_text

    def find_simple_entities(self) -> EntityDict:
        """
        Finds simple entities in text. Simple entity is unnamed none like cat, door etc.
        Entities like Smith, Brooklin street are not simple entities, there are named entities
        :return: Instance of EntityDict, that stores simple text entities
        """
        entity_dict = EntityDict()
        # найдем root (сказуемое)
        # то слово типа nsubj, obj, ..., которое с ним связано через head_id, явл. подлежащим
        # после этого также проверяется к какой части речи принадлежит слово
        for sent_index, sentence in enumerate(self.parsed_text.sents):
            for word_index, word in enumerate(sentence.tokens):
                if word.pos == 'NOUN':
                    # продолжаем читать слова, пока не закончится flat::... т.к. может быть именованой сущностью
                    entity = Entity(name=word.text,
                                    sentence_word_indexes={sent_index: [word_index]},
                                    relations=[word.rel])

                    entity_dict.add_entity(entity)

        return entity_dict