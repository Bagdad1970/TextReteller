class EntityBasic:
    def __init__(self, name, *, importance: float = 1.0, coherence: float = 1.0):
        self.name = name
        self.importance = importance
        self.coherence = coherence

    @classmethod
    def create_from_entity(cls, entity):
        return EntityBasic(
            name=entity.name, importance=entity.importance, coherence=entity.coherence
        )

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return f"name={self.name} importance={self.importance} coherence={self.coherence}"
