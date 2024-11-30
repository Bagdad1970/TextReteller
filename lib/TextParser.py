from natasha import (
    Doc,
    Segmenter,
    NewsEmbedding,
    NewsSyntaxParser,
    NewsMorphTagger
)

class TextParser:
    segmenter = Segmenter()
    embedding = NewsEmbedding()
    syntax_parser = NewsSyntaxParser(embedding)
    morph_tagger = NewsMorphTagger(embedding)

    processed_text = None

    @classmethod
    def get_processed_text(cls, text):
        if cls.processed_text is None:
            doc = Doc(text)
            doc.segment(cls.segmenter)
            doc.tag_morph(cls.morph_tagger)
            doc.parse_syntax(cls.syntax_parser)
            cls.processed_text = doc
        return cls.processed_text