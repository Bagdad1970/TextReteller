from src.CleanerRelatedTokens import CleanerRelatedTokens
from src.WeekEntityDict import WeekEntityDict
from src.TextParser import TextParser


class TextCleaner:
    def __init__(self, text_parser: TextParser, week_entity_dict: WeekEntityDict):
        self.parsed_text = text_parser.get_parsed_text()
        self.cleaner_related_tokens = CleanerRelatedTokens(self.parsed_text, week_entity_dict)
        #self.cleaner_single_week_entities = CleanerSingleWeekEntities(self.parsed_text, week_entity_dict)

        self.indexes_on_delete = self.find_indexes_on_delete()

    def get_indexes_on_delete(self):
        return self.indexes_on_delete

    def find_indexes_on_delete(self):
        indexes_on_delete_related_tokens = self.cleaner_related_tokens.find_delete_indexes()
        #indexes_on_delete_single_week_entities = self.cleaner_single_week_entities.find_delete_indexes()
        return indexes_on_delete_related_tokens

    def delete_words_by_indexes(self):
        new_text = ""
        for i, sent_indexes in enumerate(self.indexes_on_delete):
            new_sentence = ""
            for j, token in enumerate(self.parsed_text.sents[i].tokens):
                if j not in sent_indexes:  # Пропускаем индексы, которые нужно удалить
                    if token.pos != 'PUNCT':
                        new_sentence += token.text + " "
                    else:
                        new_sentence = new_sentence.rstrip() + token.text + ' '

            new_text += new_sentence

        return new_text

    def count_delete_tokens(self) -> int:
        return sum(len(index_set) for index_set in self.indexes_on_delete)

    def calculate_percentage_delete_and_original_tokens(self) -> float:
        len_delete_tokens = self.count_delete_tokens()
        len_original_tokens = sum(len(sent.tokens) for sent in self.parsed_text.sents)

        return round(len_delete_tokens / len_original_tokens * 100, 2)

