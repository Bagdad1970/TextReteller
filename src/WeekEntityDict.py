from src.EntityDict import EntityDict

class WeekEntityDict:
    def __init__(self, entity_dict: EntityDict):
        self.entity_dict = entity_dict

    def find_week_entities(self, proportion: float) -> EntityDict:
        sorted_entities = sorted(self.entity_dict, key=lambda entity: entity.total_weight)[0 : int(len(self.entity_dict) * proportion)]
        return EntityDict.create_from_list(sorted_entities)