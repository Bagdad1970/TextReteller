from src.entity_dict import EntityDict


def get_week_entities(entity_dict, proportion: float) -> EntityDict:
    week_entities = sorted(entity_dict, key=lambda entity: entity.total_weight)[
        0 : int(len(entity_dict) * proportion)
    ]
    return EntityDict.create_from_list(week_entities)


def get_strong_entities(entity_dict, proportion: float) -> EntityDict:
    strong_entities = sorted(entity_dict, key=lambda entity: entity.total_weight)[
        int(len(entity_dict) * proportion) :
    ]
    return EntityDict.create_from_list(strong_entities)
