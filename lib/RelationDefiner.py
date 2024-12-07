from natasha.doc import DocToken
from lib.SentenceDict import SentenceDict
from lib.EntityDict import EntityDict
from lib.TextParser import TextParser
from lib.Entity import Entity
from pymorphy3 import MorphAnalyzer
from EntityVertex import EntityVertex

class RelationDefiner:
    morph = MorphAnalyzer()
    relations_importance = {"nsubj": 6, "obj": 5, "iobj": 4, "obl": 3,
                            "nmod": 2, "amod": 1, "nsubj:pass": 6
                            }

    def __init__(self, *, text: str, entity_dict: EntityDict, sentence_dict: SentenceDict):
        self.entity_dict = entity_dict
        self.parsed_text = TextParser.get_parsed_text(text)
        self.sentence_dict = sentence_dict

    @classmethod
    def to_normal_form(cls, doc_token: DocToken):
        return cls.morph.parse(doc_token.text)[0].normal_form

    @staticmethod
    def id_to_index(id: str) -> int:
        return int(id.split('_')[1]) - 1

    @classmethod
    def sort_entity_importance_by_relation(cls, tokens: list[DocToken]) -> list:
        """
        Сортирует токены по важности rels в предложении, у которых head_id явл. одинаковый глагол
        :param tokens: Токены одинакового глагола
        :return: Список индексов отсортированных по rels
        """
        token_rels = [(cls.id_to_index(token.id), cls.relations_importance[token.rel]) for token in tokens]
        return [token[0] for token in sorted(token_rels, key=lambda x: x[1], reverse=True)]

    @classmethod
    def verbs_dependencies_in_sentence(cls, tokens: list) -> dict:
        verbs_dict = dict()

        for token in tokens:
            if token.pos == 'NOUN':  # добавить PROPN (?)
                try:
                    dependency_index = cls.id_to_index(token.head_id)
                    dependency = tokens[dependency_index]
                    if dependency.pos == 'VERB':
                        verb_text = dependency.text
                        if verb_text not in verbs_dict:
                            verbs_dict[verb_text] = [token]
                        else:
                            verbs_dict[verb_text].append(token)
                except (IndexError, ValueError):
                    pass

        return verbs_dict

    def entities_dependent_from_verbs_in_sentence(self, sent_index: int, tokens: list):
        dependency_groups = []

        verbs_in_sentence = self.verbs_dependencies_in_sentence(tokens)
        for verb, nouns in verbs_in_sentence.items():
            print(nouns)
            sorted_by_rels_indexes = self.sort_entity_importance_by_relation(nouns)

            for indexes in zip(sorted_by_rels_indexes, sorted_by_rels_indexes[1:]):
                # добавить обработку nsubj
                dependency = self.parsed_text.sents[sent_index].tokens[indexes[0]]
                dependent = self.parsed_text.sents[sent_index].tokens[indexes[1]]
                dependency_groups.append((self.to_normal_form(dependency), self.to_normal_form(dependent)))

        return dependency_groups

    @classmethod
    def entities_dependent_from_nouns_in_sentence(cls, tokens: list) -> list:
        dependency_groups = []

        for token in tokens:
            if token.pos == 'NOUN':  # добавить PROPN (?)
                try:
                    dependency_index = cls.id_to_index(token.head_id)
                    dependency = tokens[dependency_index]
                    if dependency.pos == 'NOUN':
                        dependency_groups.append((cls.morph.parse(token.text)[0].normal_form, cls.morph.parse(dependency.text)[0].normal_form))
                except (IndexError, ValueError):
                    pass

        return dependency_groups

    def dependencies_between_entities(self) -> list:
        total_dependents = []
        for sent_index, sentence in enumerate(self.parsed_text.sents):
            tokens = sentence.tokens

            dependent_from_verbs = self.entities_dependent_from_verbs_in_sentence(sent_index, tokens)
            dependent_from_nouns = self.entities_dependent_from_nouns_in_sentence(tokens)

            for entity_dependence in dependent_from_verbs + dependent_from_nouns:
                total_dependents.append(entity_dependence)

        return total_dependents

    def define_relations(self):
        # будем хранить по индексу массива список всех имен сущностей, которые там встречаются
        # по relation определим какую роль они играют в предложении
        # в соответствии с этим выделим слабосвязанные и сильносвязанные сущности
        return self.dependencies_between_entities()