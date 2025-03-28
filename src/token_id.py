class TokenID:

    @staticmethod
    def get_sentence_index(id: str) -> int:
        return int(id.split('_')[0]) - 1

    @staticmethod
    def get_word_index(id: str) -> int:
        return int(id.split('_')[1]) - 1

    @staticmethod
    def get_tuple_index(id: str) -> tuple[int, int]:
        splitted_id = id.split('_')
        return int(splitted_id[0]) - 1, int(splitted_id[1]) - 1