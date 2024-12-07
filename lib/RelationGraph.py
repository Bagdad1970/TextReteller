import networkx
from EntityVertex import EntityVertex

class RelationGraph:
    Graph = networkx.Graph()

    def __init__(self, couples_of_vertex: list[EntityVertex, [None, EntityVertex]]):
        self.couples_of_vertex = couples_of_vertex

    def create_graph(self):
        for couple_vertex in self.couples_of_vertex:
            vertex_dependency, vertex_dependent = couple_vertex

            if vertex_dependency in self.Graph.nodes:
                node_data = self.Graph.nodes[vertex_dependency]
                node_data['data'].is_nsubj = node_data['data'].is_nsubj or vertex_dependency.is_nsubj
            else:
                self.Graph.add_node(vertex_dependency, data=vertex_dependency)

            if vertex_dependent is not None:
                if vertex_dependent in self.Graph.nodes:
                    node_data = self.Graph.nodes[vertex_dependent]
                    node_data['data'].is_nsubj = node_data['data'].is_nsubj or vertex_dependent.is_nsubj
                else:
                    self.Graph.add_node(vertex_dependent, data=vertex_dependent)

                self.Graph.add_edge(vertex_dependency, vertex_dependent)

    def __str__(self):
        nodes_str = "Nodes in the graph:\n" + "\n".join(str(node) for node in self.Graph.nodes)
        edges_str = "Edges in the graph:\n" + "\n".join(
            f"Edge between {edge[0]} and {edge[1]}"
            for edge in self.Graph.edges(data=True)
        )
        return nodes_str + "\n\n" + edges_str

