from src.entity_dict import EntityDict
from src.text_parser import TextParser
from src.finders.entity_finder import EntityFinder
from src.entities.entity import Entity


def test_finding_simple_entities():
    text_parser = TextParser("Кошки не едят овощные овощи. Собаки едят мясное мясо. Кошка играется с собакой.")
    entity_finder = EntityFinder(text_parser.get_parsed_text())

    sut = entity_finder.find_simple_entities()

    assert sut == EntityDict.create_from_list(
        [
            Entity(name="кошка", sentence_word_indexes={0: [0], 2: [0]}, relations=["nsubj", "nsubj"]),
            Entity(name="овощ", sentence_word_indexes={0: [4]}, relations=["obj"]),
            Entity(name="собака", sentence_word_indexes={1: [0], 2: [3]}, relations=["nsubj", "obj"]),
            Entity(name="мясо", sentence_word_indexes={1: [3]}, relations=["obj"]),
        ]
    )
