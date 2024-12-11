from TextParser import TextParser
from lib.EntityDict import EntityDict
from lib.NameNormalizer import NameNormalizer
from lib.TokenID import TokenID


class CleanerRelatedTokens(TokenID, NameNormalizer):
    def __init__(self, text, week_entity_dict: EntityDict):
        self.parsed_text = TextParser.get_parsed_text(text)
        self.week_entity_dict = week_entity_dict
        self.indexes_on_delete = [[] for _ in range(len(self.parsed_text.sents))]

    def find_token_associated_forward_with_week_entity(self, sent_index: int, word_index: int):
        """
        Поиск токена, являющегося зависимостью слабой сущности.
        :param sent_index: Индекс предложения, в котором находится слабой сущности
        :param word_index: Индекс слова слабой сущности
        :return: Токен зависимости слабой сущности
        """
        entity_token = self.parsed_text.sents[sent_index].tokens[word_index]
        sent_index, word_index = self.id_to_tuple_index(entity_token.head_id)
        return self.parsed_text.sents[sent_index].tokens[word_index]

    def get_entities_associated_with_dependency(self, dependency_id: str) -> list:
        dependency_sent_index = self.id_to_sentence_index(dependency_id)
        return list(filter(lambda token: token.pos == 'NOUN' and token.head_id == dependency_id,
                               self.parsed_text.sents[dependency_sent_index].tokens))

    def get_dependent_tokens(self, token) -> list:
        token_id = token.id
        token_sent_index = self.id_to_sentence_index(token_id)
        return [dependent_token for dependent_token in self.parsed_text.sents[token_sent_index].tokens if dependent_token.head_id == token_id]

    def recursive_token_descent(self, token, depth: int, visited=None):
        if visited is None:
            visited = set()

        if token.id in visited:
            return None

        visited.add(token.id)

        if depth > 0:
            token_sent_index, token_word_index = self.id_to_tuple_index(token.id)
            self.indexes_on_delete[token_sent_index].append(token_word_index)  # добавляем индексы токена

            if token.pos == 'VERB':
                # если встречается глагол, то необходимо для него найти список всех сущностей, зависимых от него
                associated_entities = self.get_entities_associated_with_dependency(token.id)
                depth += 1
                for associated_entity in associated_entities:
                    self.recursive_token_descent(associated_entity, depth, visited)

            elif token.pos == 'NOUN' or token.pos == 'PROPN':
                # если все сущности слабые, то продолжаем рекурсивно добавлять индексы
                normalized_name = self.name_to_normal_form(token.text)
                if self.week_entity_dict.is_entity_name(normalized_name):
                    # если некоторые сущности явл. сильными, то для них спуск прекращается,
                    # а для слабых продолжается и множество индексов очищается
                    self.indexes_on_delete[token_sent_index].clear()
                else:
                    dependent_tokens = self.get_dependent_tokens(token)
                    depth += 1
                    for dependent_token in dependent_tokens:
                        self.recursive_token_descent(dependent_token, depth, visited)
            else:
                dependent_tokens = self.get_dependent_tokens(token)
                depth += 1
                for dependent_token in dependent_tokens:
                    self.recursive_token_descent(dependent_token, depth, visited)
        else:
            dependent_tokens = self.get_dependent_tokens(token)
            depth += 1
            for dependent_token in dependent_tokens:
                self.recursive_token_descent(dependent_token, depth, visited)

    def find_dependents(self, associated_entities: list):
        if associated_entities:
            for entity in associated_entities:
                self.recursive_token_descent(entity, 0)


    def find_delete_indexes(self) -> list:
        # если и зависимость слабой сущности является слабой, то и её можно удалить
        for entity in self.week_entity_dict:
            for sent_index, word_indexes in entity.sentence_word_indexes.items():
                for word_index in word_indexes:
                    # ищем относительно позиции сущности
                    dependency_of_week_entity = self.find_token_associated_forward_with_week_entity(sent_index, word_index)
                    associated_entities = self.get_entities_associated_with_dependency(dependency_of_week_entity.id)
                    self.find_dependents(associated_entities)

        return self.indexes_on_delete