from natasha import Doc, NewsSyntaxParser, NewsEmbedding, Segmenter, NewsMorphTagger


class TextParser:
    segmenter = Segmenter()
    embedding = NewsEmbedding()
    morph_tagger = NewsMorphTagger(embedding)
    syntax_parser = NewsSyntaxParser(embedding)

    def __init__(self, text: str):
        self.parsed_text = self.parse_text(text)

    @classmethod
    def parse_text(cls, text: str):
        if text == "":
            raise ValueError("Invalid text")

        doc = Doc(text)
        doc.segment(cls.segmenter)
        doc.tag_morph(cls.morph_tagger)
        doc.parse_syntax(cls.syntax_parser)
        return doc

    def get_parsed_text(self) -> Doc:
        return self.parsed_text
