from natasha.doc import DocToken
from src.entity_dict import EntityDict
from src.word_normalizer import WordNormalizer
from src.token_id import TokenID

class RelationDefiner(TokenID, WordNormalizer):
    relations_importance = {"nsubj": 6, "obj": 5, "iobj": 4, "obl": 3,
                            "nmod": 2, "amod": 1, "nsubj:pass": 6
                            }

    def __init__(self, parsed_text, entity_dict: EntityDict):
        self.parsed_text = parsed_text
        self.entity_dict = entity_dict

    @classmethod
    def sort_entity_importance_by_relation(cls, tokens: list[DocToken]) -> list:
        """
        Сортирует токены по важности rels в предложении, у которых head_id явл. одинаковым глаголом
        :param tokens: Токены одинакового глагола
        :return: Список индексов отсортированных по rels
        """
        token_rels = [(cls.get_word_index(token.id), cls.relations_importance[token.rel]) for token in tokens]
        return [token[0] for token in sorted(token_rels, key=lambda x: x[1], reverse=True)]

    @classmethod
    def verbs_dependencies_in_sentence(cls, tokens: list) -> dict:
        verbs_dict = dict()

        for token in tokens:
            if token.pos == 'NOUN':  # добавить PROPN (?)
                try:
                    dependency_index = cls.get_word_index(token.head_id)
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

    def entities_dependent_from_verbs_in_sentence(self, sent_index: int, tokens: list) -> list:
        """
        Ищет зависимые от глаголов сущности.
        :param sent_index: Индекс текущего обрабатываемого предложения
        :param tokens: Список токенов текущего предложения
        :return: Список кортежей зависимостей (левый элемент является зависимостью правого)
        """
        dependency_groups = []

        verbs_in_sentence = self.verbs_dependencies_in_sentence(tokens)
        for verb, nouns in verbs_in_sentence.items():
            sorted_by_rels_indexes = self.sort_entity_importance_by_relation(nouns)

            for indexes in zip(sorted_by_rels_indexes, sorted_by_rels_indexes[1:]):
                dependency, dependent = self.parsed_text.sents[sent_index].tokens[indexes[0]], self.parsed_text.sents[sent_index].tokens[indexes[1]]

                dependency_groups.append((self.name_to_normal_form(dependency.text), self.name_to_normal_form(dependent.text)))

        return dependency_groups

    def recursive_iter(self, token: DocToken, depth: int, visited=None):
        if visited is None:
            visited = set()

        if token.id in visited:
            return None

        visited.add(token.id)

        if depth > 3:
            return None
        elif 0 < depth <= 3:
            if token.pos == 'VERB':
                return None
            elif token.pos == 'NOUN':
                return token
            else:
                splitted_head_id = tuple(token.head_id.split('_'))
                head_token_sent_index, head_token_word_index = int(splitted_head_id[0]) - 1, int(splitted_head_id[1]) - 1
                head_token = self.parsed_text.sents[head_token_sent_index].tokens[head_token_word_index]
                depth += 1
                return self.recursive_iter(head_token, depth, visited)
        else:
            splitted_head_id = tuple(token.head_id.split('_'))
            head_token_sent_index, head_token_word_index = int(splitted_head_id[0]) - 1, int(splitted_head_id[1]) - 1
            head_token = self.parsed_text.sents[head_token_sent_index].tokens[head_token_word_index]
            depth += 1
            return self.recursive_iter(head_token, depth, visited)

    def entities_dependent_from_nouns_in_sentence(self, tokens: list) -> list:
        dependency_groups = []

        for token in tokens:  # tokens - массив зависимых токенов
            if token.pos == 'NOUN':  # добавить PROPN (?)
                try:
                    # dependency - зависимость token
                    dependent_token = self.recursive_iter(token, 0)
                    if dependent_token is not None:
                        dependency_groups.append((self.morph.parse(dependent_token.text)[0].normal_form, self.morph.parse(token.text)[0].normal_form))
                except (IndexError, ValueError):
                    pass

        return dependency_groups

    def transform_to_entity_vertexes(self, couple_entity_names: tuple[str, str]) -> tuple:
        dependency, dependent = couple_entity_names
        dependency_entity_main, dependent_entity_main = (self.entity_dict[dependency].separate_entity_main(),
                                                             self.entity_dict[dependent].separate_entity_main())

        return dependency_entity_main, dependent_entity_main

    def relations_of_entities(self) -> list:
        # будем хранить по индексу массива список всех имен сущностей, которые там встречаются
        # по relation определим какую роль они играют в предложении
        # в соответствии с этим выделим слабосвязанные и сильносвязанные сущности
        total_dependents = []
        for sent_index, sentence in enumerate(self.parsed_text.sents):
            tokens = sentence.tokens

            dependent_from_verbs = self.entities_dependent_from_verbs_in_sentence(sent_index, tokens)
            dependent_from_nouns = self.entities_dependent_from_nouns_in_sentence(tokens)

            for couple_entities in dependent_from_verbs + dependent_from_nouns:
                couple_entity_vertexes = self.transform_to_entity_vertexes(couple_entities)
                total_dependents.append(couple_entity_vertexes)

        return total_dependents

