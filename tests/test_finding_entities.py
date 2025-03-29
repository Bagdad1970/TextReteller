import pytest

from src.entity_dict import EntityDict
from src.text_parser import TextParser
from src.entity_finder import EntityFinder
from src.entity import Entity


def test_finding_simple_entities():
    text_parser = TextParser("Кошки не едят овощные овощи. Собаки едят мясное мясо.")
    entity_finder = EntityFinder(text_parser)

    sut = entity_finder.find_simple_entities()

    assert sut == EntityDict.create_from_list(
        [
            Entity(name="кошка", sentence_word_indexes={0: [0]}, relations=["nsubj"]),
            Entity(name="овощ", sentence_word_indexes={0: [4]}, relations=["obj"]),
            Entity(name="собака", sentence_word_indexes={1: [0]}, relations=["nsubj"]),
            Entity(name="мясо", sentence_word_indexes={1: [3]}, relations=["obj"]),
        ]
    )
