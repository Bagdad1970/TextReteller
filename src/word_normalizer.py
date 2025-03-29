from pymorphy3 import MorphAnalyzer

class NameNormalizer:
    morph = MorphAnalyzer()

    @classmethod
    def name_to_normal_form(cls, name):
        return cls.morph.parse(name)[0].normal_form