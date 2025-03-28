import re

import natasha.obj
from natasha import (
    Doc,
    Segmenter,
    MorphVocab,
    NamesExtractor
)

morph_vocab = MorphVocab()
segmenter = Segmenter()
names_extractor = NamesExtractor(morph_vocab)

class NameSynonyms:
    def __init__(self, name: str):
        self.name = name.strip()

    def get_name_from_extractor(self):
        # проходимся наташей
        doc = Doc(self.name)
        doc.segment(segmenter)

        return [match.fact for match in names_extractor(doc.text)][0]

    def check_correct_natasha_processing(self, name):
        part_names_counter = 0
        for attr, value in name.__dict__.items():
            print(attr, value)
            if value is not None:
                part_names_counter += 1

        if len(self.name.split()) == part_names_counter:
            return True
        return False

    def get_surname(self):
        splitted_name = self.name.split(' ')
        if len(splitted_name) >= 3:
            index = [i for i, word in enumerate(splitted_name) if re.fullmatch(r'[а-я]+', word)][0]
            if index != -1:
                return ' '.join(splitted_name[index : ])

        return splitted_name[-1]

    def get_lastname(self):
        pass

    def get_surname_and_firstname(self):
        # Фрэнк Каупервуд (анг)
        # Каупервуд Фрэнк (ру)
        # Иван Иванов (ру)
        name = self.get_name_from_extractor()
        if self.check_correct_natasha_processing(name):
            return {'surname': name.last, 'firstname': name.first, 'lastname': name.middle}
        else:
            return {'surname': name.first, 'firstname': name.last, 'lastname': self.get_lastname()}

    def name_synonyms(self):
        pass

name_synonyms = NameSynonyms('Фрэнк Алджернон Каупервуд')
#name = name_synonyms.get_name_from_extractor()
#print(name)
#print(name_synonyms.check_correct_natasha_processing(name))

print(name_synonyms.get_surname_and_firstname())