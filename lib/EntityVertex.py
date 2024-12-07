from dataclasses import dataclass
from Entity import Entity

@dataclass
class EntityVertex:
    name: str
    weight: float
    is_nsubj: bool

    def __init__(self, *, entity: Entity, is_nsubj: bool = False):
        self.name = entity.name
        self.weight = entity.weight
        self.is_nsubj = is_nsubj

    def __hash__(self):
        return hash((self.name, self.weight))

    def __eq__(self, other):
        return self.name == other.name and self.weight == other.weight

    def __str__(self):
        return (f"Name: {self.name} "
                f"Weight: {self.weight} "
                f"Is_nsubj: {self.is_nsubj} ")
