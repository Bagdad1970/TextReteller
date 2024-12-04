from lib.Entity import Entity
from lib.EntityDict import EntityDict

class SentenceDict:
    def __init__(self, entity_dict):
        self.sentence_dict = self.match_sentences_with_entities(entity_dict)

    @property
    def items(self):
        return self.sentence_dict.items()

    @staticmethod
    def match_sentences_with_entities(entity_dict: EntityDict) -> dict:
        """
        Соотносит сущности с предложениями в которых они встречаются
        :return: Словарь номеров предложений и сущностей в них
        """
        def clear_from_repeated_entities(entities_in_sentences: dict) -> None:
            for key, entity_names in entities_in_sentences.items():
                unique_entity_names = []
                for name in entity_names:
                    if name not in unique_entity_names:
                        unique_entity_names.append(name)

                entities_in_sentences[key] = unique_entity_names

        entities_in_sentences = dict()
        for entity in entity_dict:
            for sent_index, word_indexes in entity.sentence_word_indexes.items():
                if sent_index not in entities_in_sentences:
                    entities_in_sentences[sent_index] = [entity.name]
                else:
                    entities_in_sentences[sent_index].append(entity.name)

        clear_from_repeated_entities(entities_in_sentences)

        return entities_in_sentences

    def __str__(self):
        return "\n".join(f"{key}: {words}" for key, words in self.sentence_dict.items())