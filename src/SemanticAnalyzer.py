from ImportanceCounter import ImportanceCounter
from RelationDefiner import RelationDefiner
from EntityDict import EntityDict

class SemanticAnalyzer:
    def __init__(self, text: str, entities: EntityDict):
        self.entities = entities
        self.importance_finder = ImportanceCounter(entities)
        self.relation_definer = RelationDefiner(text=text, entity_dict=self.entities)

    def importance_of_entities(self):
        self.importance_finder.find_weights()

    def relation_of_entities(self):
        return self.relation_definer.relations()