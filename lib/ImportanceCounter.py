from lib.Entity import Entity
from lib.EntityDict import EntityDict
from lib.TextSplitter import TextSplitter
import json

def load_config(path):
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)

class ImportanceCounter:
    COORDINATING_CONJUCTIONS = [
        "и", "да", "но", "а", "зато", "или", "либо", "ни", "то",
        "не то", "то ли", "как",
    ]
    SUBORDIRATING_CONJUCTIONS = [
        "что", "чтобы", "как", "когда", "пока", "ли", "будто", "если", "раз",
        "хотя", "пусть", "несмотря на то что", "так как", "потому что", "поскольку",
        "чем", "как будто", "точно", "едва", "лишь", "только", "для того чтобы",
        "с тех пор как", "до тех пор пока", "как только", "столько сколько",
        "так что", "где", "куда", "откуда", "зачем", "почему"
    ]
    MAX_COORDINATING_CONJUCTIONS_SIZE = max([len(conj.split()) for conj in COORDINATING_CONJUCTIONS])
    MAX_SUBORDIRATING_CONJUCTIONS_SIZE = max([len(conj.split()) for conj in SUBORDIRATING_CONJUCTIONS])

    def __init__(self, text, entity_dict: EntityDict):
        self.metrics = load_config('../config/entity_metrics.json')
        self.entity_dict = entity_dict
        self.tokenized_text = TextSplitter(text).split_text_on_words()

    @staticmethod
    def find_nearest_comma(*, tokens: list[str]) -> int:
        """"""
        nearest_comma_index = -1
        for i in range(len(tokens) - 1, -1, -1):
            if tokens[i] == ',':
                nearest_comma_index = i
                break

        return nearest_comma_index

    def define_entity_part(self, sentence_index, word_index, comma_index) -> str:
        """"""
        words_after_comma = self.tokenized_text[sentence_index][comma_index+1 : word_index]

        for i in range(0, len(words_after_comma)):
            conjuctions_size = len(words_after_comma[0: i])
            conjuctions = ' '.join(words_after_comma[0 : i])
            if (conjuctions_size > self.MAX_COORDINATING_CONJUCTIONS_SIZE and
                    conjuctions_size > self.MAX_SUBORDIRATING_CONJUCTIONS_SIZE):
                return 'unknown_part'
            else:
                if conjuctions in self.COORDINATING_CONJUCTIONS:
                    return 'coordinate'
                elif conjuctions in self.SUBORDIRATING_CONJUCTIONS:
                    return 'subordinate'

    def define_sentence_part_entity(self):
        """Определяет в какой части предложения (сочинительаня, основная) находится сущность"""
        # проходимся по каждому индексу в entity_dict
        # смотрим это значение в tokenized_text
        # находим ближайшие знак препинания и какой он
        # смотрим есть ли слово перед самой сущностью, описывающее часть предложения этой сущности
        for entity in self.entity_dict:
            for tuple_index in entity.sentence_word_indexes:
                sentence_index, word_index = tuple_index[0], tuple_index[1]
                nearest_comma_index = self.find_nearest_comma(tokens=self.tokenized_text[sentence_index][0 : word_index])
                if nearest_comma_index != -1:
                    entity_part = self.define_entity_part(sentence_index, word_index, nearest_comma_index)
                    entity.weight += self.metrics[entity_part]
                else:
                    entity.weight += self.metrics['main']

        for entity in self.entity_dict:
            entity.weight = entity.weight / len(entity.sentence_word_indexes)

        return self.entity_dict