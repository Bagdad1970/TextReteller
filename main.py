from src.entities.entity import Entity
from src.entity_finder import EntityFinder
from src.semantic_processing.semantic_analyzer import SemanticAnalyzer
from src.semantic_processing.relation_graph import RelationGraph
from src.text_parser import TextParser
import src.entities_by_proportion as week_entities



def main():
    text = ("Котенок Мурзик любит играть с клубком ниток. "
            "Он часто бегает к хозяину и прячется за диваном. "
            "Иногда Мурзик залезает на шторы и смотрит на нитки. "
            "Вечером он пьет молоко и мурлычет на коленях у хозяина. "
            "Мурзик — самый веселый и ласковый питомец."
            )

    text_parser = TextParser(text)
    print(text_parser.get_parsed_text())
    entities_correlation = 0.8

    parsed_text = text_parser.get_parsed_text()

    entity_finder = EntityFinder(parsed_text)
    entity_dict = entity_finder.find_simple_entities()

    semantic_analyzer = SemanticAnalyzer(parsed_text, entity_dict)
    semantic_analyzer.importance_of_entities()
    couples_of_vertex = semantic_analyzer.relation_of_entities()

    graph = RelationGraph(couples_of_vertex)
    graph.traverse_and_update_coherence()
    weighted_vertexes = graph.get_weighted_vertexes()

    entity_dict.attach_entity_mains(weighted_vertexes)

    _week_entities = week_entities.get_week_entities(entity_dict, entities_correlation)
    _strong_entities = week_entities.get_strong_entities(entity_dict, entities_correlation)

    print(len(entity_dict))
    print(len(_week_entities))
    print(len(_strong_entities))
    print(_week_entities)
    print(f"\n\n\n{_strong_entities}")

if __name__ == '__main__':
    main()