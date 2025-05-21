from .entity_finder import EntityFinder
from .text_parser import TextParser
import entities_by_proportion
from .text_shortener import TextShortener
import semantic_processing as semantics


def short_text(text: str, correlation: float) -> str:
    text_parser = TextParser(text)
    parsed_text = text_parser.get_parsed_text()

    parsed_text.syntax.print()

    entity_finder = EntityFinder(parsed_text)
    entity_dict = entity_finder.find_simple_entities()

    semantic_analyzer = semantics.SemanticAnalyzer(parsed_text, entity_dict)
    semantic_analyzer.importance_of_entities()
    couples_of_vertex = semantic_analyzer.relation_of_entities()

    graph = semantics.RelationGraph(couples_of_vertex)
    graph.traverse_and_update_coherence()
    weighted_vertexes = graph.get_weighted_vertexes()

    entity_dict.attach_entity_mains(weighted_vertexes)

    _week_entities = entities_by_proportion.get_weak_entities(entity_dict, correlation)
    _strong_entities = entities_by_proportion.get_strong_entities(entity_dict, correlation)

    text_shortener = TextShortener(
        parsed_text=parsed_text,
        entity_dict=entity_dict,
        weak_entity_dict=_week_entities
    )

    return text_shortener.short_text()