from nltk import sent_tokenize, word_tokenize

def split_text_on_sentences(text: str) -> list:
    return sent_tokenize(text)

def split_sentence_on_words(sentence: str) -> list:
    return word_tokenize(sentence)