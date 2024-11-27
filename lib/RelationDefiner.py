from lib.EntityDict import EntityDict
from lib.config_reader import load_config

class RelationDefiner:
    def __init__(self, entity_dict: EntityDict):
        self.metrics = load_config('relation_metrics.json')
        self.entity_dict = entity_dict

    def define_relations(self):
        pass

