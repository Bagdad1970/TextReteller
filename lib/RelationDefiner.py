from natasha.doc import DocToken

from lib.EntityDict import EntityDict
from lib.Config import Config
from lib.TextParser import TextParser
from lib.Entity import Entity


class RelationDefiner(Config):
    def __init__(self, text: str, entity_dict: EntityDict):
        self.metrics = Config.load_config('relation_metrics.json')
        self.entity_dict = entity_dict
        self.parsed_text = TextParser.get_processed_text(text)

        print(self.entity_dict['планета'])

    def match_sentences_with_entities(self) -> dict:
        """
        Соотносит сущности с предложениями в которых они встречаются
        :return: Словарь номеров предложений и сущностей в них
        """
        entities_in_sentences = dict()

        for entity in self.entity_dict:
            for i, sentence_word_index in enumerate(entity.sentence_word_indexes):
                if sentence_word_index[0] not in entities_in_sentences:
                    entities_in_sentences[sentence_word_index[0]] = [ entity.name ]
                else:
                    entities_in_sentences[sentence_word_index[0]].append( entity.name )

        return entities_in_sentences

    def count_middle_entities(self):

        def recursive_iter(doc_token: DocToken, visited=None) -> int:
            if visited is None:
                visited = set()  # Инициализация множества для отслеживания посещённых токенов

            # Если токен уже был обработан, прекращаем рекурсию
            if doc_token.id in visited:
                return 0

            visited.add(doc_token.id)

            if doc_token.rel == 'root':
                return 0
            else:
                splitted_head_id = doc_token.head_id.split('_')
                next_sent_index, next_word_index = int(splitted_head_id[0]) - 1, int(splitted_head_id[1]) - 1
                next_token = self.parsed_text.sents[next_sent_index].tokens[next_word_index]
                if doc_token.id == doc_token.head_id:  # если происходит зацикливание
                    return recursive_iter(self.parsed_text.sents[next_sent_index].tokens[next_word_index - 1], visited)
                elif doc_token.pos == 'NOUN':
                    return 1 + recursive_iter(next_token, visited)
                else:
                    return recursive_iter(next_token, visited)


        def count_chain(sent_index: int, entity: Entity) -> None:
            # берем word_index по sent_index в entity
            # считаем кол-во слов от этого id до root
            word_indexes = [sentence_word_index[1] for sentence_word_index in entity.sentence_word_indexes if sentence_word_index[0] == sent_index]

            # запускаем рекурсвиный обход
            for word_index in word_indexes:
                chain_length = recursive_iter(self.parsed_text.sents[sent_index].tokens[word_index])
                entity.chain_lengths.append(chain_length)


        # берем сущности, находящиеся в одном предложении
        # считаем кол-во сущнсотей лежащих между ними через head_id и id
        matched_sentences = self.match_sentences_with_entities()

        for sent_index, entity_names in matched_sentences.items():
            # ищем длину цепочки для каждой пары сущностей
            for entity_name in entity_names:
                print(entity_name)
                # что делать, если сущность встрчечается 2 раза в предложении
                count_chain(sent_index, self.entity_dict[entity_name])


    def define_relations(self):
        # будем хранить по индексу массива список всех имен сущностей, которые там встречаются
        # по relation определим какую роль они играют в предложении
        # в соответствии с этим выделим слабосвязанные и сильносвязанные сущности

        matched_entities = self.match_sentences_with_entities()
        self.count_middle_entities()
        print(matched_entities)



