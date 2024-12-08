from dataclasses import dataclass
from Entity import Entity

@dataclass
class EntityVertex:
    name: str
    weight: float
    weight_graph: float

    def __init__(self, entity: Entity):
        self.name = entity.name
        self.weight = entity.weight
        self.weight_graph = 0.0

    def set_weight_graph(self, weight_graph):
        self.weight_graph = weight_graph

    def __hash__(self):
        return hash((self.name, self.weight))

    def __eq__(self, other):
        return self.name == other.name and self.weight == other.weight

    def __str__(self):
        return (f"Name: {self.name} "
                f"Weight: {self.weight} "
                f"Weight_Graph: {self.weight_graph}"
                )
