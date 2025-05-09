from src.entity_dict import EntityDict


def get_weak_entities(entity_dict, proportion: float) -> EntityDict:
    week_entities = sorted(entity_dict.values(), key=lambda entity: entity.total_weight)[
        0 : int(len(entity_dict) * proportion)
    ]
    return EntityDict(week_entities)


def get_strong_entities(entity_dict, proportion: float) -> EntityDict:
    strong_entities = sorted(entity_dict.values(), key=lambda entity: entity.total_weight)[
        int(len(entity_dict) * proportion) :
    ]
    return EntityDict(strong_entities)
