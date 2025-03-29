from src.entity_dict import EntityDict

def get_week_entities(entity_dict, proportion: float) -> EntityDict:
    sorted_entities = sorted(entity_dict, key=lambda entity: entity.total_weight)[0 : int(len(entity_dict) * proportion)]
    return EntityDict.create_from_list(sorted_entities)