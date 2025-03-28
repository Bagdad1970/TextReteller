from src.Entity import Entity
from src.TokenID import TokenID
from src.NameNormalizer import NameNormalizer
from src.EntityDict import EntityDict


class CleanerSingleWeekEntities(TokenID, NameNormalizer):
    def __init__(self, parsed_text, week_entity_dict: EntityDict):
        self.parsed_text = parsed_text
        self.week_entity_dict = week_entity_dict

        self.indexes_on_delete = [set() for _ in range(len(self.parsed_text.sents))]

    def count_dependencies_of_entity_in_sentence(self, sent_index: int, entity: Entity):
        entity_word_indexes = entity.sentence_word_indexes[sent_index]
        entity_word_indexes_counter = {word_index: 0 for word_index in entity_word_indexes}
        print(entity_word_indexes_counter)
        for token in self.parsed_text.sents[sent_index].tokens:
            token_head_index = self.id_to_word_index(token.head_id)
            if token_head_index in entity_word_indexes:
                print(token.text, token_head_index)
                entity_word_indexes_counter[token_head_index] += 1

        return filter(lambda word_index: entity_word_indexes_counter[word_index] == 0, entity_word_indexes_counter)

    def find_delete_indexes(self):
        for sent_index, sentence in enumerate(self.parsed_text.sents):
            week_entities_in_sentence = []
            for week_entity in self.week_entity_dict:
                if sent_index in week_entity.sentence_word_indexes:
                    week_entities_in_sentence.append(week_entity)

            print(week_entities_in_sentence)

            #week_entities_in_sentence = [week_entity for week_entity in self.week_entity_dict if week_entity.sentence_word_indexes[sent_index]]
            #print(week_entities_in_sentence)
            for week_entity in week_entities_in_sentence:
                single_entities = self.count_dependencies_of_entity_in_sentence(sent_index, week_entity)
                print(single_entities)




