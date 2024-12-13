from natasha import Doc, NewsSyntaxParser, NewsEmbedding, Segmenter, NewsMorphTagger

class TextParser:
    segmenter = Segmenter()
    embedding = NewsEmbedding()
    morph_tagger = NewsMorphTagger(embedding)
    syntax_parser = NewsSyntaxParser(embedding)

    parsed_text = None

    @classmethod
    def get_parsed_text(cls, text: str = ''):
        if text != '':
            cls.set_parsed_text(text)
        return cls.parsed_text

    @classmethod
    def set_parsed_text(cls, new_text):
        doc = Doc(new_text)
        doc.segment(cls.segmenter)
        doc.tag_morph(cls.morph_tagger)
        doc.parse_syntax(cls.syntax_parser)
        cls.parsed_text = doc