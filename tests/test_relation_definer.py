from src.finders.entity_finder import EntityFinder
from src.semantic_processing.relation_definer import RelationDefiner
from src.text_parser import TextParser


class TestRelationDefiner:
    sentence = (
        "После проверки документов, включающих отчёты, счета-фактуры и акты сверки, "
        "бухгалтер сообщил руководству, "
        "что обнаружены расхождения в данных по поставкам товаров и оплате услуг."
    )
    parsed_sentence_tokens = TextParser(sentence).get_parsed_text().sents[0].tokens
    parsed_text = TextParser(sentence).get_parsed_text()

    def test_verbs_dependencies_in_sentence(self):
        sut = RelationDefiner.nouns_depends_from_verbs_in_sentence(
            self.parsed_sentence_tokens
        )

        assert sut == {
            "обнаружены": [
                self.parsed_sentence_tokens[18],
                self.parsed_sentence_tokens[20],
            ],
            "сообщил": [
                self.parsed_sentence_tokens[1],
                self.parsed_sentence_tokens[12],
                self.parsed_sentence_tokens[14],
            ],
        }

    def test_sort_entity_importance_by_relation(self):
        verbs_dependencies = RelationDefiner.nouns_depends_from_verbs_in_sentence(
            self.parsed_sentence_tokens
        )["сообщил"]

        sut = RelationDefiner.sort_entity_importance_by_relation(verbs_dependencies)

        assert sut == [12, 14, 1]

    def test_entities_dependent_from_verbs_in_sentence(self):
        simple_entities = EntityFinder(self.parsed_text).find_simple_entities()
        relation_definer = RelationDefiner(self.parsed_text, simple_entities)

        sut = relation_definer.arrange_dependencies_between_nouns_by_priority(
            0, self.parsed_sentence_tokens
        )

        assert sut == [
            ("бухгалтер", "руководство"),
            ("руководство", "проверка"),
            ("расхождение", "данные"),
        ]

    def test_nouns_dependent_from_nouns_in_sentence(self):
        simple_entities = EntityFinder(self.parsed_text).find_simple_entities()
        relation_definer = RelationDefiner(self.parsed_text, simple_entities)

        sut = relation_definer.nouns_dependent_from_nouns_in_sentence(
            self.parsed_sentence_tokens
        )

        assert sut == [
            ("проверка", "документ"),
            ("отчёт", "акт"),
            ("акт", "сверка"),
            ("данные", "поставка"),
            ("поставка", "товар"),
            ("поставка", "оплата"),
            ("оплата", "услуга"),
        ]
