from natasha.doc import DocToken, Doc
from src.entity_dict import EntityDict
from src.word_normalizer import WordNormalizer
from src.token_id import TokenID


class RelationDefiner(TokenID, WordNormalizer):
    relations_priority = {
        "nsubj": 6,
        "obj": 5,
        "iobj": 4,
        "obl": 3,
        "nmod": 2,
        "amod": 1,
        "nsubj:pass": 6,
    }

    def __init__(self, parsed_text: Doc, entity_dict: EntityDict):
        self.__parsed_text = parsed_text
        self.__entity_dict = entity_dict

    @classmethod
    def sort_entity_importance_by_relation(cls, tokens: list[DocToken]) -> list:
        """
        Сортирует токены по приоритету rels в предложении, у которых head_id явл. одинаковым глаголом
        :param tokens: Токены одинакового глагола
        :return: Список индексов отсортированных по rels
        """
        token_rels = [
            {
                "id": TokenID.get_word_index(token.id),
                "rel": cls.relations_priority[token.rel],
            }
            for token in tokens
        ]
        sorted_in_descending_by_priority = sorted(
            token_rels, key=lambda x: x.get("rel"), reverse=True
        )
        return [token.get("id") for token in sorted_in_descending_by_priority]

    @classmethod
    def nouns_depends_from_verbs_in_sentence(cls, tokens: list) -> dict:
        """
        Finds all verbs and nouns that depend on them in sentence
        :param tokens: all tokens in sentence
        :return: dictionary of verbs and nouns
        """
        verbs_dict = dict()

        noun_tokens = filter(
            lambda token: token.pos == "NOUN", tokens
        )  # добавить PROPN (?)
        for token in noun_tokens:
            try:
                dependency_index = TokenID.get_word_index(token.head_id)
                dependency = tokens[dependency_index]
                if dependency.pos == "VERB":
                    if "acl" not in dependency.rel:  # consider only verbs
                        verb_word = dependency.text
                        if verb_word not in verbs_dict:
                            verbs_dict[verb_word] = [token]
                        else:
                            verbs_dict[verb_word].append(token)
            except (IndexError, ValueError):
                pass

        return verbs_dict

    def arrange_dependencies_between_nouns_by_priority(
        self, sent_index: int, tokens: list
    ) -> list:
        """
        Arranges dependencies between nouns by priority
        i.e. cat eats meat -> [(cat, meat)] because cat is nsubj (priority=6), meat is obj (priority=5)
        :param sent_index: Sentence index
        :param tokens: Sentence tokens
        :return: List of nouns tuples where left element is dependency and right is dependent
        """
        dependency_groups = []

        verb_nouns_in_sentence = self.nouns_depends_from_verbs_in_sentence(tokens)
        for verb, nouns in verb_nouns_in_sentence.items():
            sorted_by_rels_indexes = self.sort_entity_importance_by_relation(nouns)

            associated_noun_pairs = zip(
                sorted_by_rels_indexes, sorted_by_rels_indexes[1:]
            )
            for indexes in associated_noun_pairs:
                current_sentence_tokens = self.__parsed_text.sents[sent_index].tokens

                dependency, dependent = (
                    current_sentence_tokens[indexes[0]],
                    current_sentence_tokens[indexes[1]],
                )
                dependency_groups.append(
                    (
                        WordNormalizer.word_to_normal_form(dependency.text),
                        WordNormalizer.word_to_normal_form(dependent.text),
                    )
                )

        return dependency_groups

    def __recursive_iter(self, token: DocToken, depth: int, visited=None):
        if visited is None:
            visited = set()

        if token.id in visited or depth > 3:
            return None

        visited.add(token.id)

        if 1 <= depth <= 3:
            if token.pos == "VERB":
                return None
            elif token.pos == "NOUN":
                return token

        head_token_sent_index, head_token_word_index = TokenID.get_tuple_index(
            token.head_id
        )
        head_token = self.__parsed_text.sents[head_token_sent_index].tokens[
            head_token_word_index
        ]
        return self.__recursive_iter(head_token, depth + 1, visited)

    def nouns_dependent_from_nouns_in_sentence(self, tokens: list) -> list:
        """
        Finds tuples of nouns where left noun is dependency for right noun
        i.e. в "оплата услуг" услуга зависимо от оплаты
        :param tokens: Sentence tokens
        :return: List tuples of nouns
        """
        dependency_groups = []

        noun_tokens = filter(lambda token: token.pos == "NOUN", tokens)
        for noun_token in noun_tokens:  # tokens - массив зависимых токенов
            try:
                # dependency - зависимость token
                dependent_token = self.__recursive_iter(noun_token, 0)
                if dependent_token is not None:
                    dependency_groups.append(
                        (
                            WordNormalizer.word_to_normal_form(dependent_token.text),
                            WordNormalizer.word_to_normal_form(noun_token.text),
                        )
                    )
            except (IndexError, ValueError):
                pass

        return dependency_groups

    def get_entity_vertexes(self, pair_entity_names: tuple[str, str]) -> tuple:
        """
        Reduces associated entity names to instances of EntityBasic
        :param pair_entity_names: A pair of associated nouns
        :return: Tuple with two instances of EntityBasic
        """
        dependency, dependent = pair_entity_names
        dependency_entity_main, dependent_entity_main = (
            self.__entity_dict[dependency].separate_entity_basic(),
            self.__entity_dict[dependent].separate_entity_basic(),
        )

        return dependency_entity_main, dependent_entity_main

    def relations_of_entities(self) -> list:
        # будем хранить по индексу массива список всех имен сущностей, которые там встречаются
        # по relation определим какую роль они играют в предложении
        # в соответствии с этим выделим слабосвязанные и сильно-связанные сущности
        total_dependents = []
        for sent_index, sentence in enumerate(self.__parsed_text.sents):
            tokens = sentence.tokens

            dependent_from_verbs = self.arrange_dependencies_between_nouns_by_priority(
                sent_index, tokens
            )
            dependent_from_nouns = self.nouns_dependent_from_nouns_in_sentence(tokens)

            for couple_entities in dependent_from_verbs + dependent_from_nouns:
                couple_entity_vertexes = self.get_entity_vertexes(couple_entities)
                total_dependents.append(couple_entity_vertexes)

        return total_dependents
