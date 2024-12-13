from src.SimpleEntityFinder import SimpleEntityFinder
from src.TextParser import TextParser


class EntityFinder:
    def __init__(self, text_parser: TextParser):
        parsed_text = text_parser.get_parsed_text()
        self.simple_entity_finder = SimpleEntityFinder(parsed_text)

    def find_entities(self):
        return self.simple_entity_finder.find_entities()