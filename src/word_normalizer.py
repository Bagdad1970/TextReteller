from pymorphy3 import MorphAnalyzer

class WordNormalizer:
    morph = MorphAnalyzer()

    @classmethod
    def word_to_normal_form(cls, name):
        return cls.morph.parse(name)[0].normal_form