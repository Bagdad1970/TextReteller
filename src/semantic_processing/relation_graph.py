from src.entities.entity_basic import EntityBasic
import networkx
from collections import deque


class RelationGraph:
    def __init__(self, couples_of_vertex: list[tuple[EntityBasic, EntityBasic]]):
        self.Graph = networkx.Graph()
        self.__create_graph(couples_of_vertex)

    def __create_graph(self, vertex_pairs: list[tuple[EntityBasic, EntityBasic]]):
        for vertex_pair in vertex_pairs:
            vertex_dependency, vertex_dependent = vertex_pair
            self.Graph.add_node(vertex_dependency)
            self.Graph.add_node(vertex_dependent)
            self.Graph.add_edge(vertex_dependency, vertex_dependent)

    def find_max_vertex_in_component(self, graph_component) -> EntityBasic:
        """
        Finds vertex with the maximum count of degrees.
        :param graph_component: The concrete graph component with some vertexes.
        :return: Vertex with the maximum edges count
        """

        max_vertex = None
        max_degree = -1

        for vertex in graph_component:
            if self.Graph.degree[vertex] > max_degree:
                max_degree = self.Graph.degree[vertex]
                max_vertex = vertex

        return max_vertex

    def calculate_max_depth_in_component(self, start_vertex: EntityBasic) -> int:
        """
        Calculates maximum depth in component from any vertex.
        Maximum depth is the number of vectors of the longest chain from start_vertex to the extreme ones.
        :param start_vertex: Vertex from which the countdown will be conducted
        :return: Max depth in component from start_vertex
        """

        visited = set()
        queue = deque([(start_vertex, 0)])  # (текущая вершина, глубина)
        max_distance = 0

        while queue:
            current_vertex, distance = queue.popleft()

            if current_vertex in visited:
                continue

            visited.add(current_vertex)

            if distance > max_distance:
                max_distance = distance

            for neighbour in self.Graph.neighbors(current_vertex):
                if neighbour not in visited:
                    queue.append((neighbour, distance + 1))

        return max_distance

    def traverse_and_update_coherence(self):
        """
        Updates coherence for every vertex in components.
        Coherence computes by the formula 1 - depth / (max_depth + 1)
        :return:
        """
        visited = set()

        for component in networkx.connected_components(self.Graph):
            start_vertex = self.find_max_vertex_in_component(component)
            max_depth = self.calculate_max_depth_in_component(start_vertex)

            queue = deque([(start_vertex, 0)])

            while queue:
                current_vertex, depth = queue.popleft()

                if current_vertex in visited:
                    continue

                current_vertex.coherence = 1 - depth / (max_depth + 1)
                visited.add(current_vertex)

                for neighbour in self.Graph.neighbors(current_vertex):
                    if neighbour not in visited:
                        queue.append((neighbour, depth + 1))

    def get_weighted_vertexes(self):
        return self.Graph.nodes

    def __str__(self):
        nodes_str = "Nodes in the graph:\n" + "\n".join(
            str(node) for node in self.Graph.nodes
        )
        edges_str = "Edges in the graph:\n" + "\n".join(
            f"Edge between {edge[0]} and {edge[1]}"
            for edge in self.Graph.edges(data=True)
        )
        return nodes_str + "\n\n" + edges_str
