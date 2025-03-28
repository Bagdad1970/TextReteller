from src.Entity import Entity
from EntityDict import EntityDict
import stanza

class NamedEntityFinder:
    def __init__(self, text):
        self.text = text

    def get_named_entities(self) -> list[dict]:
        nlp = stanza.Pipeline(lang='ru', download_method=None, processors='tokenize, ner')
        return nlp(self.text).entities

    @staticmethod
    def processing_entities(entities: list) -> EntityDict:
        entity_dict = EntityDict()
        for named_entity in entities:
            entity = Entity(name=named_entity['name'], type=named_entity['type'])

            # присваивание индексов

            entity_dict.add_entity(entity)

        return entity_dict

    def find_entities(self) -> EntityDict:
        named_entities = self.get_named_entities()
        entity_dict = self.processing_entities(named_entities)

        return entity_dict
