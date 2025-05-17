from src.semantic_processing.importance_counter import ImportanceCounter
from src.semantic_processing.relation_definer import RelationDefiner
from src.entity_dict import EntityDict
from natasha import Doc


class SemanticAnalyzer:
    def __init__(self, parsed_text: Doc, entities: EntityDict):
        self.importance_finder = ImportanceCounter(parsed_text, entities)
        self.relation_definer = RelationDefiner(parsed_text, entities)

    def importance_of_entities(self):
        self.importance_finder.calculate_importance()

    def relation_of_entities(self):
        return self.relation_definer.relations_of_entities()
