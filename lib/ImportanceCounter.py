from lib.EntityDict import EntityDict
from lib.TextSplitter import TextSplitter
from lib.Config import Config

class ImportanceCounter:
    def __init__(self, text, entity_dict: EntityDict):
        self.metrics = Config.load_config('entity_metrics.json')
        self.entity_dict = entity_dict
        self.tokenized_text = TextSplitter(text).split_text_on_words()

    def find_weights(self) -> None:
        for entity in self.entity_dict:
            summary_weight = sum([self.metrics[relation] for relation in entity.relations])
            entity.weight = summary_weight