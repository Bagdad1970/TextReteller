from Entity import Entity

class EntityDict:
    def __init__(self):
        self.entities = dict()

    def add_entity(self, new_entity: Entity):
        if new_entity.name not in self.entities:
            self.entities[new_entity.name] = new_entity
        else:
            sentence_word_index = new_entity.sentence_word_indexes[-1]
            relation = new_entity.relations[-1]
            #associated_entity_name = new_entity.associated_entity_names[-1]
            #synonym = new_entity.synonyms[-1]
            self.entities[new_entity.name].add_features(sentence_word_index=sentence_word_index, relation=relation)

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