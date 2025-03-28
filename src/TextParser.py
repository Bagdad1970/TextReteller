from natasha import Doc, NewsSyntaxParser, NewsEmbedding, Segmenter, NewsMorphTagger

class TextParser:
    segmenter = Segmenter()
    embedding = NewsEmbedding()
    morph_tagger = NewsMorphTagger(embedding)
    syntax_parser = NewsSyntaxParser(embedding)

    def __init__(self, text):
        self.parsed_text = self.parse_text(text)

    def parse_text(self, text: str):
        if text == '':
            pass # raise Exception
        doc = Doc(text)
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)
        doc.parse_syntax(self.syntax_parser)
        return doc

    def get_parsed_text(self) -> Doc:
        return self.parsed_text