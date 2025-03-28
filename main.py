from src.EntityFinder import EntityFinder
from src.SemanticAnalyzer import SemanticAnalyzer
from src.RelationGraph import RelationGraph
from src.TextCleaner import TextCleaner
from src.TextParser import TextParser
from src.WeekEntityDict import WeekEntityDict

class Main:
    def __init__(self, text, entities_correlation: float = 0.5):
        self.text_parser = TextParser(text)
        self.entities_correlation = entities_correlation

        self.amount_delete_tokens = 0
        self.percentage_delete_and_original_tokens = 0

    def reduce_text(self):
        entity_finder = EntityFinder(self.text_parser)
        entity_dict = entity_finder.find_entities()

        semantic_analyzer = SemanticAnalyzer(self.text_parser, entity_dict)
        semantic_analyzer.importance_of_entities()
        couples_of_vertex = semantic_analyzer.relation_of_entities()

        graph = RelationGraph(couples_of_vertex)
        graph.traverse_and_update_depth()
        weighted_vertexes = graph.get_weighted_vertexes()

        entity_dict.attach_entity_mains(weighted_vertexes)

        week_entity_finder = WeekEntityDict(entity_dict)
        week_entities = week_entity_finder.find_week_entities(self.entities_correlation)

        text_cleaner = TextCleaner(self.text_parser, week_entities)

        self.amount_delete_tokens = text_cleaner.count_delete_tokens()
        self.percentage_delete_and_original_tokens = text_cleaner.calculate_percentage_delete_and_original_tokens()

        return text_cleaner.delete_words_by_indexes()

    def count_delete_tokens(self) -> int:
        return self.amount_delete_tokens

    def count_percentage_delete_and_original_tokens(self) -> float:
        return self.percentage_delete_and_original_tokens