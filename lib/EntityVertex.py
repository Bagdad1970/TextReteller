from dataclasses import dataclass
from Entity import Entity

@dataclass
class EntityVertex:
    name: str
    weight: float

    def __init__(self, entity: Entity):
        self.name = entity.name
        self.weight = entity.weight

    def __hash__(self):
        return hash((self.name, self.weight))

    def __str__(self):
        return (f"Name: {self.name}"
                f"Weight: {self.weight}")
