from lib.Entity import Entity
from lib.EntityMain import EntityMain

class EntityDict:
    def __init__(self):
        self.entities = dict()

    def add_entity(self, new_entity: Entity):
        """
        Adds entity to the entities
        :param new_entity: Instance of Entity
        """
        if new_entity.name not in self.entities:
            self.entities[new_entity.name] = new_entity
        else:
            self.entities[new_entity.name].add_indexes(new_entity.sentence_word_indexes)
            self.entities[new_entity.name].add_relations(new_entity.relations)

    def attach_entity_mains(self, entity_mains: list[EntityMain]):
        for entity_main in entity_mains:
            self.entities[entity_main.name].attach_entity_main(entity_main)

    def __getattr__(self, name):
        if name in self.entities:
            return self.entities[name]
        raise AttributeError(f"No entity found with name '{name}'")

    def __getitem__(self, name):
        if name in self.entities:
            return self.entities[name]
        raise KeyError(f"No entity found with name '{name}'")

    def __iter__(self):
        return iter(self.entities.values())

    def __len__(self):
        return len(self.entities)

    def __add__(self, other):  # объединение двух словарей
        # проверка наличия одинаковых Entity и объединение их
        pass

    def __str__(self):
        return "\n\n".join(str(entity) for entity in self.entities.values())