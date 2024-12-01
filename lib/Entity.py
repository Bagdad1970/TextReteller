from dataclasses import dataclass

@dataclass
class Entity:
    """Class for keeping data of entity"""
    name: str
    synonyms: list[str]
    type: str
    sentence_word_indexes: dict[int, list]
    relations: list[str]
    weight: float
    chain_lengths: dict[int, list]

    def __init__(self, *, name: str, type: str = '', weight: float = 0.0):
        self.name = name.lower()
        self.synonyms = []
        self.type = type
        self.sentence_word_indexes = dict()
        self.weight = weight
        self.relations = []
        self.chain_lengths = dict()

    @staticmethod
    def get_name_synonyms(name: str) -> list[str]:
        return []

    def add_index(self, sent_index: int, word_index: int):
        if sent_index not in self.sentence_word_indexes:
            self.sentence_word_indexes[sent_index] = [ word_index ]
        else:
            self.sentence_word_indexes[sent_index].append(word_index)

    def add_indexes(self, sent_word_indexes: dict[int, list]):
        for sent_index, word_indexes in sent_word_indexes.items():
            if sent_index not in self.sentence_word_indexes:
                self.sentence_word_indexes[sent_index] = word_indexes
            else:
                for word_index in word_indexes:
                    self.sentence_word_indexes[sent_index].append(word_index)

    def add_relation(self, relation: str):
        if relation is not None and relation != '':
            self.relations.append(relation)

    def add_synonym(self, synonym: str):
        if synonym != '' and synonym is not None:
            self.synonyms.append(synonym)

    def add_features(self, *, sentence_word_indexes: dict[int, list] = None, relation: str = None, synonym: str = None):
        self.add_indexes(sentence_word_indexes)
        self.add_relation(relation)
        self.add_synonym(synonym)

    def __ne__(self, other):
        return self.name != other.name

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return (f"Name: {self.name}\n"
                f"Type: {self.type}\n"
                f"List of tuple indexes: {self.sentence_word_indexes}\n"
                f"Weight: {self.weight}\n"
                f"Relations: {self.relations}\n"
                f"Chain lengths: {self.chain_lengths}\n")