from dataclasses import dataclass

@dataclass
class Entity:
    """Class for keeping data of entity"""
    name: str
    synonyms: list[str]
    type: str
    sentence_word_indexes: list[tuple[int, int]]
    relations: list[str]
    associated_entity_names: list[tuple[str, float]]
    weight: float

    def __init__(self, *, name: str, type: str = '', weight: float = 0.0):
        self.name = name.lower()
        self.synonyms = []
        self.type = type
        self.sentence_word_indexes = []
        self.weight = weight
        self.relations = []
        self.associated_entity_names = []

    @staticmethod
    def get_name_synonyms(name: str) -> list[str]:
        return []

    def add_index(self, sentence_word_index: tuple[int, int]):
        if sentence_word_index is not None:
            self.sentence_word_indexes.append(sentence_word_index)

    def add_relation(self, relation: str):
        if relation is not None and relation != '':
            self.relations.append(relation)

    def add_associated_entity(self, associated_entity_name: tuple[str, float]):
        if associated_entity_name is not None:
            self.associated_entity_names.append(associated_entity_name)

    def add_synonym(self, synonym: str):
        if synonym != '' and synonym is not None:
            self.synonyms.append(synonym)

    def add_features(self, *, sentence_word_index: tuple[int, int] = None, relation: str = None, associated_entity_name: tuple[str, float] = None, synonym: str = None):
        self.add_index(sentence_word_index)
        self.add_relation(relation)
        self.add_associated_entity(associated_entity_name)
        self.add_synonym(synonym)

    def __str__(self):
        return (f"Name: {self.name}\n"
                f"Type: {self.type}\n"
                f"List of tuple indexes: {self.sentence_word_indexes}\n"
                f"Weight: {self.weight}\n"
                f"Relations: {self.relations}\n"
                f"Associated_entity_names: {self.associated_entity_names}\n")