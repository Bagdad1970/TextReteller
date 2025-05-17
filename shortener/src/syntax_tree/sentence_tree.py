from anytree import RenderTree
from natasha.doc import DocToken
from src.syntax_tree.token_node import TokenNode


class SentenceTree:
    """Builds syntax tree for a sentence"""

    def __init__(self, tokens: list[DocToken]):
        self.__nodes = [TokenNode(token) for token in tokens]
        self.root = self.__build_tree()

    def __build_tree(self) -> TokenNode:
        """Constructs the tree structure by setting parent-child relationships"""
        for node in self.__nodes:
            if node.data.head_id != '0':  # Skip root node
                parent = next((n for n in self.__nodes if n.data.id == node.data.head_id), None)
                if parent:
                    node.parent = parent

        return next((node for node in self.__nodes if node.data.rel == 'root'))

    def print_tree(self):
        if self.root:
            for pre, _, node in RenderTree(self.root):
                print(f"{pre}{node}")
        else:
            print("No root node found - tree is empty")

    def find_nodes(self, **attributes) -> list[TokenNode]:
        """Finds nodes matching specified attributes (e.g., pos='NOUN', rel='nsubj')"""
        return [node for node in self.__nodes
                if all(getattr(node.data, attr) == value
                       for attr, value in attributes.items())]