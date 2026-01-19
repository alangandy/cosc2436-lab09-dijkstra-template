"""
Lab 09: Dijkstra's Algorithm
Implement Dijkstra's shortest path from Chapter 9.

Chapter 9 covers:
- Weighted graphs
- Dijkstra's algorithm for shortest path
- Difference from BFS (BFS = unweighted, Dijkstra = weighted)
"""
from typing import Dict, List, Tuple, Optional
import heapq


def dijkstra(graph: Dict[str, Dict[str, int]], start: str, end: str) -> Tuple[Optional[int], List[str]]:
    """
    Find shortest path in weighted graph using Dijkstra's algorithm.
    
    From Chapter 9: Dijkstra's works with weighted graphs where
    edges have different costs/distances.
    
    Args:
        graph: Adjacency list with weights {node: {neighbor: weight}}
        start: Starting node
        end: Target node
    
    Returns:
        Tuple of (total_cost, path) or (None, []) if no path
    
    Example:
        >>> graph = {"a": {"b": 6, "c": 2}, "b": {"d": 1}, "c": {"b": 3, "d": 5}, "d": {}}
        >>> dijkstra(graph, "a", "d")
        (6, ['a', 'c', 'b', 'd'])
    """
    # TODO: Implement Dijkstra's algorithm
    # 1. Initialize costs dict: start=0, others=infinity
    # 2. Initialize parents dict to track path
    # 3. Use priority queue (heapq) for efficiency
    # 4. While queue not empty:
    #    a. Pop node with lowest cost
    #    b. If it's the end, reconstruct path
    #    c. For each neighbor, calculate new cost
    #    d. If new cost < known cost, update and add to queue
    # 5. Reconstruct path from parents
    
    pass


def build_path(parents: Dict[str, str], start: str, end: str) -> List[str]:
    """Reconstruct path from parents dictionary."""
    # TODO: Build path from end back to start using parents
    pass
