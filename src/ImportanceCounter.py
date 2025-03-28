from src.EntityDict import EntityDict
from src.Config import Config
from src.Entity import Entity


class ImportanceCounter(Config):
    metrics = Config.load_config('entity_metrics.json')

    def __init__(self, parsed_text, entity_dict: EntityDict):
        self.parsed_text = parsed_text
        self.entity_dict = entity_dict

    def importance_for_entity(self, entity: Entity) -> float:
        relation_sum = 0
        try:
            for relation in entity.relations:
                relation_sum += self.metrics[relation]
        except KeyError:
            pass

        amount_sents_in_text = len(self.parsed_text.sents)
        return relation_sum / amount_sents_in_text

    def count_importances(self) -> None:
        for entity in self.entity_dict:
            entity.importance = self.importance_for_entity(entity)