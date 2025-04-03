from src.entity_finder import EntityFinder
from src.semantic_analyzer import SemanticAnalyzer
from src.relation_graph import RelationGraph
from src.text_parser import TextParser
import src.week_entities as week_entities

class Main:
    def __init__(self, text, entities_correlation: float = 0.5):
        self.text_parser = TextParser(text)
        self.entities_correlation = entities_correlation


    def reduce_text(self):
        entity_finder = EntityFinder(self.text_parser.get_parsed_text())
        entity_dict = entity_finder.find_simple_entities()

        semantic_analyzer = SemanticAnalyzer(self.text_parser, entity_dict)
        semantic_analyzer.importance_of_entities()
        couples_of_vertex = semantic_analyzer.relation_of_entities()

        graph = RelationGraph(couples_of_vertex)
        graph.traverse_and_update_coherence()
        weighted_vertexes = graph.get_weighted_vertexes()

        entity_dict.attach_entity_mains(weighted_vertexes)

        _week_entities = week_entities.get_week_entities(entity_dict, self.entities_correlation)

        return week_entities