"""Lab 09: Test Cases for Dijkstra's Algorithm"""
import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dijkstra import dijkstra


# Graph from Chapter 9
GRAPH = {
    "start": {"a": 6, "b": 2},
    "a": {"fin": 1},
    "b": {"a": 3, "fin": 5},
    "fin": {}
}


class TestDijkstra:
    def test_basic_path(self):
        cost, path = dijkstra(GRAPH, "start", "fin")
        assert cost == 6  # start -> b -> a -> fin = 2 + 3 + 1
        assert path == ["start", "b", "a", "fin"]
    
    def test_direct_path(self):
        graph = {"a": {"b": 5}, "b": {}}
        cost, path = dijkstra(graph, "a", "b")
        assert cost == 5
        assert path == ["a", "b"]
    
    def test_no_path(self):
        graph = {"a": {}, "b": {}}
        cost, path = dijkstra(graph, "a", "b")
        assert cost is None
        assert path == []
    
    def test_same_node(self):
        cost, path = dijkstra(GRAPH, "start", "start")
        assert cost == 0
        assert path == ["start"]
    
    def test_longer_graph(self):
        graph = {
            "Houston": {"Dallas": 240, "Austin": 165},
            "Dallas": {"Austin": 195, "El Paso": 570},
            "Austin": {"El Paso": 530},
            "El Paso": {}
        }
        cost, path = dijkstra(graph, "Houston", "El Paso")
        assert cost == 695  # Houston -> Austin -> El Paso


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
