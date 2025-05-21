from anytree import PreOrderIter
from .syntax_tree.sentence_tree import SentenceTree
from .entity_dict import EntityDict
from .syntax_tree.token_node import TokenNode
from .token_id import TokenID


class TextShortener(TokenID):

    def __init__(self, parsed_text, entity_dict: EntityDict, weak_entity_dict: EntityDict):
        self.parsed_text = parsed_text
        self.entity_dict = entity_dict
        self.weak_entity_dict = weak_entity_dict


    @staticmethod
    def does_sentence_contains_only_verb(root: TokenNode) -> bool:
        entities_counter = len( [ node for node in PreOrderIter(root)
                                  if node.data.pos == 'NOUN' ] )
        return entities_counter == 0


    def does_sentence_contains_only_weak_entities(self, root: TokenNode) -> bool:
        """
        If sentence contains only weak entities, it can be removed full without additional checks.
        :param root: root of sentence
        :return: True if sentence contains only weak entities, otherwise - False
        """
        week_entities_counter = entities_counter = 0
        for node in PreOrderIter(root):
            if node.data.pos == 'NOUN':
                if self.weak_entity_dict.is_entity_name_in_dict(node.data.text):
                    week_entities_counter += 1
                if self.entity_dict.is_entity_name_in_dict(node.data.text):
                    entities_counter += 1

        return week_entities_counter == entities_counter


    def mark_deleting_entities(self, node: TokenNode, deleting_node: TokenNode = None) -> None:
        """
        Marks in sentence tree weak entities and tokens that depends on it.
        But if after week entity goes strong entity, week entity will not be deleted.
        :param node: checking node
        :param deleting_node: deleting node ancestor
        """
        if not node.children and node.data.pos != 'NOUN':
            pass
        else:
            if node.data.pos == 'NOUN':
                if self.weak_entity_dict.is_entity_name_in_dict(node.data.text):
                    node.is_deleting_node = True
                    for child in node.children:
                        self.mark_deleting_entities(child, node)
                else:
                    if deleting_node is not None:
                        deleting_node.is_deleting_node = False
                    for child in node.children:
                        self.mark_deleting_entities(child, None)
            else:
                for child in node.children:
                    self.mark_deleting_entities(child, deleting_node)


    def mark_deleting_verbs(self, node: TokenNode):
        """
        Marks verbs in a sentence who's all children are weak creatures.
        :param node: current node
        """
        if not node.children and node.data.pos == 'VERB':
            node.is_deleting_node = True

        if node.data.pos == 'VERB':
            if len([child for child in node.children
                    if child.is_deleting_node == True and child.data.pos != 'PUNCT' ]) == len([ node for node in node.children if node.data.pos != 'PUNCT'] ):
                node.is_deleting_node = True
            for child in node.children:
                self.mark_deleting_verbs(child)


    def mark_deleting_tokens_in_sentence(self, node: TokenNode) -> None:
        self.mark_deleting_entities(node, None)
        self.mark_deleting_verbs(node)


    @staticmethod
    def find_deleting_indexes_in_sentence(root: TokenNode) -> set:
        """
        Finds indexes in sentence that will be deleted.
        It collects all indexes, that are descendants of weak entities.
        :param root: root of sentence
        :return: set of indexes to delete
        """

        def collect_deleting_indexes(node: TokenNode, deleting_indexes: set) -> set:
            deleting_indexes.add(TokenID.get_word_index(node.data.id))
            if node.children:
                for child in node.children:
                    collect_deleting_indexes(child, deleting_indexes)
            return deleting_indexes

        indexes = set()
        for node in PreOrderIter(root):
            if node.is_deleting_node:
                dependent_tokens_indexes_to_delete = collect_deleting_indexes(node, set())
                if dependent_tokens_indexes_to_delete is not None:
                    indexes.update(dependent_tokens_indexes_to_delete)

        return indexes


    def find_deleting_tokens_in_text(self) -> dict[int, set]:
        indexes_in_text_to_delete = {}
        for sent_index, sentence in enumerate(self.parsed_text.sents):

            sentence_tree = SentenceTree(sentence.tokens)
            root = sentence_tree.root

            if not self.does_sentence_contains_only_verb(root):
                if self.does_sentence_contains_only_weak_entities(root):
                    indexes_in_text_to_delete[sent_index] = set(range(0, len(sentence.tokens) + 1))
                else:
                    self.mark_deleting_tokens_in_sentence(root)
                    deleting_token_indexes_in_sentence = self.find_deleting_indexes_in_sentence(root)
                    if deleting_token_indexes_in_sentence:
                        indexes_in_text_to_delete[sent_index] = deleting_token_indexes_in_sentence

        return indexes_in_text_to_delete


    def get_shortened_text(self, indexes_to_delete: dict):
        cleared_text = ""
        for sent_index, word_indexes in indexes_to_delete.items():
            cleared_sentence = ""
            for token_index, token in enumerate(self.parsed_text.sents[sent_index].tokens):
                if token_index not in word_indexes:
                    if token.pos != 'PUNCT':
                        cleared_sentence += token.text + " "
                    else:
                        cleared_sentence = cleared_sentence.rstrip() + token.text + ' '

            cleared_text += cleared_sentence.capitalize()

        return cleared_text.strip()


    def short_text(self) -> str:
        indexes_to_delete = self.find_deleting_tokens_in_text()

        return self.get_shortened_text(indexes_to_delete)