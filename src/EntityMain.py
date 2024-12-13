from dataclasses import dataclass

@dataclass
class EntityMain:
    name: str
    importance: float
    coherence: float

    def __init__(self, entity):
        self.name = entity.name
        self.importance = entity.importance
        self.coherence = entity.coherence

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return (f"Name: {self.name} "
                f"Importance: {self.importance} "
                f"Coherence: {self.coherence}"
                )
