from src.text_shortener import TextShortener
from src.finders.entity_finder import EntityFinder
from src.semantic_processing.semantic_analyzer import SemanticAnalyzer
from src.semantic_processing.relation_graph import RelationGraph
from src.text_parser import TextParser
import src.entities_by_proportion as week_entities


def main():
    text = ("Кот любит играть с клубком ниток. "
            "Он часто бегает к хозяину и прячется за диваном. "
            "Вечером он пьет молоко и мурлычет на коленях у хозяина. "
            )

    text = "В условиях непростой геополитической ситуации российско-китайская внешнеполитическая связка является стабилизирующим фактором, полагает Путин, поскольку обе страны отстаивают многополярный миропорядок. Си также говорил о многополярности и создании «инклюзивной экономической глобализации», а также о том, что Россия и Китай отстаивают многостороннюю торговую систему и бесперебойность поставок."

    text = ("Кошка кормила котят, которые затем пошли бегать по дому. Дом был очень просторным и котятам было много места для игр")

    text_parser = TextParser(text)
    entities_correlation = 0.8

    parsed_text = text_parser.get_parsed_text()

    parsed_text.syntax.print()

    entity_finder = EntityFinder(parsed_text)
    entity_dict = entity_finder.find_simple_entities()

    semantic_analyzer = SemanticAnalyzer(parsed_text, entity_dict)
    semantic_analyzer.importance_of_entities()
    couples_of_vertex = semantic_analyzer.relation_of_entities()

    graph = RelationGraph(couples_of_vertex)
    graph.traverse_and_update_coherence()
    weighted_vertexes = graph.get_weighted_vertexes()

    entity_dict.attach_entity_mains(weighted_vertexes)

    _week_entities = week_entities.get_weak_entities(entity_dict, entities_correlation)
    _strong_entities = week_entities.get_strong_entities(entity_dict, entities_correlation)

    print(entity_dict)

    text_cleaner = TextShortener(
        parsed_text=parsed_text,
        entity_dict=entity_dict,
        weak_entity_dict=_week_entities
    )

    print(text_cleaner.short_text())


if __name__ == '__main__':
    main()