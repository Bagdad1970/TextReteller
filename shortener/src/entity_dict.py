from .entities.entity import Entity
from .entities.entity_basic import EntityBasic
from collections import UserDict
from .word_normalizer import WordNormalizer


class EntityDict(UserDict, WordNormalizer):
    def __init__(self, entities: list=None):
        super().__init__()
        if entities is not None:
            for entity in entities:
                self.add_entity(entity)

    def add_entity(self, new_entity: Entity) -> None:
        """
        Adds entity to the entities
        :param new_entity: Instance of Entity
        """
        if new_entity.name not in self:
            self.data[new_entity.name] = new_entity
        else:
            self.data[new_entity.name].add_indexes(new_entity.sentence_word_indexes)
            self.data[new_entity.name].add_relations(new_entity.relations)

    def attach_entity_mains(self, entity_mains: list[EntityBasic]) -> None:
        for entity_main in entity_mains:
            self.data[entity_main.name].attach_entity_basic(entity_main)

    def is_entity_name_in_dict(self, name: str) -> bool:
        """
        Checks for the presence of a name or normalized name in dictionary
        :param name: entity name (can be not normalized)
        :return: true if dict contains that name, otherwise it is false
        """
        return (name in self.data) or (WordNormalizer.word_to_normal_form(name) in self.data)

    def __str__(self) -> str:
        return "\n\n".join(str(entity) for entity in self.data.values())