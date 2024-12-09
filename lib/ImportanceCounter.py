from lib.EntityDict import EntityDict
from lib.Config import Config
from lib.Entity import Entity
from lib.TextParser import TextParser


class ImportanceCounter(Config):
    metrics = Config.load_config('entity_metrics.json')

    def __init__(self, entity_dict: EntityDict):
        self.entity_dict = entity_dict
        self.parsed_text = TextParser.get_parsed_text()

    @staticmethod
    def count_number_of_different_sentences(entity: Entity):
        return len(set(sent_index for sent_index in entity.sentence_word_indexes.keys()))

    def weight_for_entity(self, entity) -> float:
        relation_sum = sum([self.metrics[relation] for relation in entity.relations])
        sents_with_entity = self.count_number_of_different_sentences(entity)
        sents_in_text = len(self.parsed_text.sents)
        return (relation_sum * sents_with_entity) / (sents_in_text * (1 + relation_sum))

    def find_weights(self) -> None:
        for entity in self.entity_dict:
            entity.weight_entity = self.weight_for_entity(entity)