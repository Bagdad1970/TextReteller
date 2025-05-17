import networkx
import pytest

from shortener.src.entities.entity_basic import EntityBasic
from shortener.src.semantic_processing.relation_graph import RelationGraph


@pytest.fixture
def _test_graph():
    test_edges = [
        # first component
        (EntityBasic('отчет', importance=0.5), EntityBasic('работа', importance=0.4)),
        (EntityBasic('отчет', importance=0.5), EntityBasic('зарплата', importance=0.3)),
        (EntityBasic('зарплата', importance=0.3), EntityBasic('стаж', importance=0.2)),
        (EntityBasic('стаж', importance=0.2), EntityBasic('отпуск', importance=0.1)),
        (EntityBasic('отпуск', importance=0.1), EntityBasic('отчет', importance=0.5)),
        (EntityBasic('работа', importance=0.4), EntityBasic('дедлайн', importance=0.6)),
        (EntityBasic('дедлайн', importance=0.6), EntityBasic('стресс', importance=0.3)),
        (EntityBasic('работа', importance=0.4), EntityBasic('коллеги', importance=0.3)),
        (EntityBasic('коллеги', importance=0.3), EntityBasic('совещание', importance=0.4)),
        (EntityBasic('отчет', importance=0.5), EntityBasic('коллеги', importance=0.3)),

        # mixed situation
    ]
    return RelationGraph(test_edges)

class TestRelationGraph:

    @pytest.mark.parametrize('component_num, expected', [
        (0, EntityBasic('отчет', importance=0.5)),
    ])
    def test_finding_max_vertex_in_component(self, _test_graph, component_num, expected):
        components = list(networkx.connected_components(_test_graph.Graph))
        testing_components = components[component_num]

        sut = _test_graph.find_max_vertex_in_component(testing_components)

        assert sut == expected


    @pytest.mark.parametrize('start_vertex, expected', [
        (EntityBasic('отчет', importance=0.5), 3),  # отчет -> зарплата -> стаж -> отпуск -> отчет
    ])
    def test_calculating_max_depth_in_component(self, _test_graph, start_vertex, expected):
        sut = _test_graph.calculate_max_depth_in_component(start_vertex)

        assert sut == expected
