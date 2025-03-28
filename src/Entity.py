from src.EntityMain import EntityMain
from src.NameNormalizer import NameNormalizer

class Entity(NameNormalizer):
    def __init__(self, name: str):
        self.name = self.name_to_normal_form(name)
        self.total_weight = 1.0
        self.coherence = 1.0
        self.importance = 1.0
        self.sentence_word_indexes = dict()
        self.relations = []

    def calculate_total_weight(self):
        self.total_weight = self.importance * self.coherence

    def separate_entity_main(self):
        return EntityMain(self)

    def attach_entity_main(self, entity_main: EntityMain):
        self.importance = entity_main.importance
        self.coherence = entity_main.coherence
        self.calculate_total_weight()

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

    def add_relations(self, relations: list[str]):
        if relations:
            for relation in relations:
                self.relations.append(relation)

    def add_features(self, *, sentence_word_indexes: dict[int, list] = None, relation: str = None):
        self.add_indexes(sentence_word_indexes)
        self.add_relation(relation)

    def __hash__(self):
        return hash((self.name, self.importance, self.total_weight, self.coherence, self.sentence_word_indexes, self.relations))

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return (f"Name: {self.name}\n"
                f"List of tuple indexes: {self.sentence_word_indexes}\n"
                f"Total Weight: {self.total_weight}\n"
                f"Entity Weight: {self.importance}\n"
                f"Coherence: {self.coherence}\n"
                f"Relations: {self.relations}\n")