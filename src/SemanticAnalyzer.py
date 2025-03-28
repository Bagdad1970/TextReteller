from src.ImportanceCounter import ImportanceCounter
from src.RelationDefiner import RelationDefiner
from src.EntityDict import EntityDict
from src.TextParser import TextParser


class SemanticAnalyzer:
    def __init__(self, text_parser: TextParser, entities: EntityDict):
        parsed_text = text_parser.get_parsed_text()
        self.importance_finder = ImportanceCounter(parsed_text, entities)
        self.relation_definer = RelationDefiner(parsed_text, entities)

    def importance_of_entities(self):
        self.importance_finder.count_importances()

    def relation_of_entities(self):
        return self.relation_definer.relations_of_entities()