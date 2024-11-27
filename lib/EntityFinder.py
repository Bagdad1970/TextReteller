from SimpleEntityFinder import SimpleEntityFinder
from NamedEntityFinder import NamedEntityFinder

# перед этим необходимо свернуть именованные сущности т.е. Фрэнк Алджернон Каупервуд есть единая сущность 'Фрэнк Алджернон Каупервуд'

class EntityFinder:
    def __init__(self, *, text: str):
        self.simple_entity_finder = SimpleEntityFinder(text)
        self.named_entity_finder = NamedEntityFinder(text)
        self.text = text

    def find_entities(self):
        return self.simple_entity_finder.find_entities()