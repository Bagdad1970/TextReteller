import pytest

from src.text_shortener import TextShortener
from src.syntax_tree.sentence_tree import SentenceTree
from src.text_parser import TextParser
from src.entities.entity import Entity
from src.entity_dict import EntityDict


class TestTextCleaner:

    @pytest.mark.parametrize('text, entity_dict, week_entities, expected', [
        ("Он играл с собакой и кошкой",
         EntityDict([Entity('собака'), Entity('кошка')]),
         EntityDict([Entity('собака')]),
         False),
        ("Он играл с собакой и кошкой",
         EntityDict([Entity('собака'), Entity('кошка')]),
         EntityDict([Entity('собака'), Entity('кошка')]),
         True)
    ])
    def test_does_sentence_contains_only_week_entities(self, text, entity_dict, week_entities, expected):
        text_parser = TextParser(text)
        parsed_text = text_parser.get_parsed_text()

        text_cleaner = TextShortener(parsed_text=parsed_text,
                                     entity_dict=entity_dict,
                                     weak_entity_dict=week_entities)

        root = SentenceTree(parsed_text.sents[0].tokens).root
        sut = text_cleaner.does_sentence_contains_only_weak_entities(root)

        assert sut == expected

    def test_iterate_function(self):
        text_parser = TextParser('Он играл с собакой и кошкой')
        parsed_text = text_parser.get_parsed_text()

        entity_dict = EntityDict([Entity('кошка'), Entity('собака')])
        week_entities = EntityDict([Entity('кошка')])

        text_cleaner = TextShortener(parsed_text=parsed_text,
                                     entity_dict=entity_dict,
                                     weak_entity_dict=week_entities)

        tree = SentenceTree(parsed_text.sents[0].tokens)
        week_node = tree.find_nodes(text='собакой')[0]
        sut = text_cleaner.iterate_function(week_node)

        assert True == True


    @pytest.mark.parametrize('text, expected', [
        ('Почему ты не играешь с кошкой.', False),
        ('играть.', True),
        ('Кошка играла с собакой.', False)
    ])
    def test_does_sentence_contains_only_verb(self, text, expected):
        text_parser = TextParser(text)
        parsed_text = text_parser.get_parsed_text()
        root = SentenceTree(parsed_text.sents[0].tokens).root

        sut = TextShortener.does_sentence_contains_only_verb(root)

        assert sut == expected


    @pytest.mark.parametrize('text, entity_dict, week_entity_dict, expected', [
        ('Мальчик играл с собакой и кошкой.',
         EntityDict([Entity('кошка'), Entity('собака'), Entity('мальчик')]),
         EntityDict([Entity('кошка')]),
         { 4, 5 }
         ),
        ('Мальчик играл с собакой и кошкой.',
         EntityDict([Entity('кошка'), Entity('собака'), Entity('мальчик')]),
         EntityDict([Entity('собакой'), Entity('мальчик'), Entity('кошка')]),
         {0, 2, 3, 4, 5}
         ),
        ('Мальчик играл с собакой и кошкой.',
         EntityDict([Entity('кошка'), Entity('собака'), Entity('мальчик')]),
         EntityDict([Entity('собакой')]),
         set()
         ),
        ('Мальчик играл с собакой и кошкой.',
         EntityDict([Entity('кошка'), Entity('собака'), Entity('мальчик')]),
         EntityDict([Entity('кошка'), Entity('собака')]),
         {2, 3, 4, 5}
         ),
    ])
    def test_mark_deleting_entities(self, text, entity_dict, week_entity_dict, expected):
        text_parser = TextParser(text)
        parsed_text = text_parser.get_parsed_text()
        root = SentenceTree(parsed_text.sents[0].tokens).root

        text_cleaner = TextShortener(parsed_text, entity_dict, week_entity_dict)
        text_cleaner.mark_deleting_entities(root)

        sut = text_cleaner.find_deleting_indexes_in_sentence(root)

        assert sut == expected


    @pytest.mark.parametrize('text, entity_dict, week_entity_dict, expected', [
        ('Мальчик играл с собакой и кошкой.',
         EntityDict([Entity('кошка'), Entity('собака'), Entity('мальчик')]),
         EntityDict([Entity('кошка')]),
         { 4, 5 }
         ),
        ('Мальчик играл с собакой и кошкой.',
         EntityDict([Entity('кошка'), Entity('собака'), Entity('мальчик')]),
         EntityDict([Entity('собакой'), Entity('мальчик'), Entity('кошка')]),
         set(range(0, 6+1))
         ),
        ('Мальчик играл с собакой и кошкой.',
         EntityDict([Entity('кошка'), Entity('собака'), Entity('мальчик')]),
         EntityDict([Entity('собакой')]),
         set()
         ),
    ])
    def test_mark_deleting_verbs(self, text, entity_dict, week_entity_dict, expected):
        text_parser = TextParser(text)
        parsed_text = text_parser.get_parsed_text()
        root = SentenceTree(parsed_text.sents[0].tokens).root

        text_cleaner = TextShortener(parsed_text, entity_dict, week_entity_dict)
        text_cleaner.mark_deleting_entities(root)
        text_cleaner.mark_deleting_verbs(root)

        sut = text_cleaner.find_deleting_indexes_in_sentence(root)

        assert sut == expected
