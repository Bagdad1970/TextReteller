from natasha.doc import DocToken
from anytree import NodeMixin

class TokenNode(NodeMixin):
    """Represents a single token in the syntax tree with parent-child relationships"""

    def __init__(self, data: DocToken, *, parent=None, children=None):
        super().__init__()
        self.data = data
        self.parent = parent
        self.is_deleting_node = False
        if children:
            self.children = children