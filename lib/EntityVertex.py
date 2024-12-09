from dataclasses import dataclass
from Entity import Entity

@dataclass
class EntityVertex:
    name: str
    weight_entity: float
    weight_graph: float

    def __init__(self, entity: Entity):
        self.name = entity.name
        self.weight_entity = entity.weight_entity
        self.weight_graph = 1.0

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return (f"Name: {self.name} "
                f"Weight: {self.weight_entity} "
                f"Weight_Graph: {self.weight_graph}"
                )
