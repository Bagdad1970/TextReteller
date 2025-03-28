from src.EntityMain import EntityMain
import networkx
from collections import deque

class RelationGraph:
    def __init__(self, couples_of_vertex: list[EntityMain, EntityMain]):
        self.Graph = networkx.Graph()
        self.create_graph(couples_of_vertex)

    def create_graph(self, couples_of_vertex: list[EntityMain, EntityMain]):
        for couple_vertex in couples_of_vertex:
            vertex_dependency, vertex_dependent = couple_vertex
            self.Graph.add_node(vertex_dependency)
            self.Graph.add_node(vertex_dependent)
            self.Graph.add_edge(vertex_dependency, vertex_dependent)

    def max_vertex_in_component(self, component) -> EntityMain:
        max_vertex = None
        max_weight = max_degree = -1

        for vertex in component:
            if vertex.importance > max_weight and self.Graph.degree[vertex] >= max_degree:
                max_weight = vertex.importance
                max_degree = self.Graph.degree[vertex]
                max_vertex = vertex

        return max_vertex

    def max_depth_in_component(self, start_vertex: EntityMain) -> int:
        visited = set()
        queue = deque([(start_vertex, 0)])  # (текущая вершина, глубина)
        max_distance = 0

        while queue:
            current_vertex, distance = queue.popleft()

            if current_vertex in visited:
                continue

            visited.add(current_vertex)

            # Проверяем, является ли текущая вершина самой удалённой
            if distance > max_distance:
                max_distance = distance

            for neighbor in self.Graph.neighbors(current_vertex):
                if neighbor not in visited:
                    queue.append((neighbor, distance + 1))

        return max_distance

    def traverse_and_update_depth(self):
        visited = set()

        for component in networkx.connected_components(self.Graph):
            start_vertex = self.max_vertex_in_component(component)
            max_depth = self.max_depth_in_component(start_vertex)

            queue = deque([(start_vertex, 0)])

            while queue:
                current_vertex, depth = queue.popleft()

                if current_vertex in visited:
                    continue

                current_vertex.coherence = 1 - depth / (max_depth + 1)
                visited.add(current_vertex)

                for neighbor in self.Graph.neighbors(current_vertex):
                    if neighbor not in visited:
                        queue.append((neighbor, depth + 1))

    def get_weighted_vertexes(self):
        return self.Graph.nodes

    def __str__(self):
        nodes_str = "Nodes in the graph:\n" + "\n".join(str(node) for node in self.Graph.nodes)
        edges_str = "Edges in the graph:\n" + "\n".join(
            f"Edge between {edge[0]} and {edge[1]}"
            for edge in self.Graph.edges(data=True)
        )
        return nodes_str + "\n\n" + edges_str