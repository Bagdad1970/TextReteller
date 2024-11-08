from text_tokenizer import *

def main():
    with open('dataset.txt', 'r') as file:
        text = file.read()

    file.close()

    sentences = split_text_on_sentences(text)
    print(sentences)

    tokens = split_sentence_on_words(sentences[2])
    print(tokens)

if __name__ == '__main__':
    main()