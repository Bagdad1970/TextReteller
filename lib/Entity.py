from dataclasses import dataclass

@dataclass
class Entity:
    """Class for keeping data of entity"""
    name: str
    type: str
    sentence_indexes: list
    word_indexes: list
    weight: float

    def __init__(self, *, name: str, type: str = '', weight: float = 1):
        self.name = name # определить __get__
        self.type = type
        self.sentence_indexes = []
        self.word_indexes = []
        self.weight = weight

    def __str__(self):
        return (f"Name: {self.name}\n"
                f"Type: {self.type}\n"
                f"List of sentence indexes: {self.sentence_indexes}\n"
                f"List of word indexes: {self.word_indexes}\n"
                f"Weight: {self.weight}")