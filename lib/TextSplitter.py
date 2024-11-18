from nltk.tokenize import word_tokenize, sent_tokenize

class TextSplitter:
    def __init__(self, text: str):
        self.text = text.strip()

    @classmethod
    def read_file(cls, filename: str):
        with open(filename, 'r') as file:
            text = file.read().strip()

        return cls(text)

    def split_text_on_sentences(self):
        return sent_tokenize(self.text)

    def split_text_on_words(self):
        return [word_tokenize(sentence) for sentence in self.split_text_on_sentences()]

    @classmethod
    def split_sentence_on_tokens(cls, sentence):
        return [word_tokenize(sentence)]

    def __str__(self):
        return self.text