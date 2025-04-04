from src.importance_counter import ImportanceCounter
from src.relation_definer import RelationDefiner
from src.entity_dict import EntityDict
from src.text_parser import TextParser


class SemanticAnalyzer:
    def __init__(self, text_parser: TextParser, entities: EntityDict):
        parsed_text = text_parser.get_parsed_text()
        self.importance_finder = ImportanceCounter(parsed_text, entities)
        self.relation_definer = RelationDefiner(parsed_text, entities)

    def importance_of_entities(self):
        self.importance_finder.calculate_importance()

    def relation_of_entities(self):
        return self.relation_definer.relations_of_entities()
