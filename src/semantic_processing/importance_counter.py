from src.entity_dict import EntityDict
from src.config import Config
from src.entities.entity import Entity


class ImportanceCounter(Config):
    metrics = Config.load_config("entity_metrics.json")

    def __init__(self, parsed_text, entity_dict: EntityDict):
        self.parsed_text = parsed_text
        self.entity_dict = entity_dict

    def importance_for_entity(self, entity: Entity) -> float:
        """
        Calculates importance for an entity.
        Entity importance is ratio of the total measure of the syntax roles of a word to the total number of sentences in text
        :param entity:
        :return: Ratio of total measure roles to the number sentences in text
        """

        relation_sum = 0.0

        try:
            for relation in entity.relations:
                relation_sum += self.metrics[relation]
        except KeyError:
            pass

        return relation_sum / len(self.parsed_text.sents)

    def calculate_importance(self) -> None:
        """
        Calculates importance for every entity and assigns it to the importance field of entity
        """

        for entity in self.entity_dict.values():
            entity.importance = self.importance_for_entity(entity)
