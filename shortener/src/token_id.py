class TokenID:

    @staticmethod
    def get_sentence_index(sentence_id: str) -> int:
        return int(sentence_id.split("_")[0]) - 1

    @staticmethod
    def get_word_index(word_id: str) -> int:
        return int(word_id.split("_")[1]) - 1

    @staticmethod
    def get_tuple_index(sentence_word_id: str) -> tuple[int, int]:
        splitted_id = sentence_word_id.split("_")
        return int(splitted_id[0]) - 1, int(splitted_id[1]) - 1
