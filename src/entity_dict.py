from src.entity import Entity
from src.entity_basic import EntityBasic

class EntityDict:
    def __init__(self, entities:list=None):
        self.entities = dict()

    @classmethod
    def create_from_list(cls, entities: list):
        entity_dict = cls()
        for entity in entities:
            entity_dict.add_entity(entity)
        return entity_dict

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

    def attach_entity_mains(self, entity_mains: list[EntityBasic]):
        for entity_main in entity_mains:
            self.entities[entity_main.name].attach_entity_basic(entity_main)

    def is_entity_name(self, name: str) -> bool:
        return name in self.entities

    def __getitem__(self, name: str):
        if name in self.entities:
            return self.entities[name]
        raise KeyError(f"No entity found with name '{name}'")

    def __eq__(self, other):
        return self.entities == other.entities

    def __iter__(self):
        return iter(self.entities.values())

    def __len__(self) -> int:
        return len(self.entities)

    def __str__(self):
        return "\n\n".join(str(entity) for entity in self.entities.values())