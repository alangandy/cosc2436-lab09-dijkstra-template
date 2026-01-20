#!/usr/bin/env python3
"""
Lab 09: Dijkstra's Algorithm - Interactive Tutorial
====================================================

🎯 GOAL: Implement Dijkstra's shortest path algorithm in dijkstra.py

📚 DIJKSTRA'S ALGORITHM (Chapter 9):
------------------------------------
Finds the shortest path in a WEIGHTED graph.

BFS vs DIJKSTRA:
- BFS: Unweighted graphs (all edges cost 1)
- Dijkstra: Weighted graphs (edges have different costs)

EXAMPLE: Finding fastest route on a map
- BFS finds fewest roads
- Dijkstra finds shortest total distance

HOW TO RUN:
-----------
    python main.py           # Run this tutorial
    python -m pytest tests/ -v   # Run the grading tests
"""

import heapq
from dijkstra import dijkstra, build_path


def print_header(title: str) -> None:
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def weighted_graphs_intro() -> None:
    """Introduce weighted graphs."""
    print_header("WEIGHTED GRAPHS")
    
    print("""
    UNWEIGHTED GRAPH (BFS):
    
        A --- B --- D
        |     |
        C ----+
    
    All edges have the same "cost" (1 step)
    
    WEIGHTED GRAPH (Dijkstra):
    
        A --6-- B --1-- D
        |       |
        2       3
        |       |
        C --5---+
    
    Edges have different costs (distances, times, etc.)
    
    PYTHON REPRESENTATION:
    ----------------------
    # Unweighted: dict of lists
    graph = {
        "A": ["B", "C"],
        "B": ["A", "C", "D"],
        ...
    }
    
    # Weighted: dict of dicts (nested dictionaries!)
    graph = {
        "A": {"B": 6, "C": 2},      # A→B costs 6, A→C costs 2
        "B": {"D": 1},               # B→D costs 1
        "C": {"B": 3, "D": 5},       # C→B costs 3, C→D costs 5
        "D": {}                      # D has no outgoing edges
    }
    """)
    
    # Live demo
    print("ACCESSING WEIGHTED GRAPH:")
    graph = {
        "A": {"B": 6, "C": 2},
        "B": {"D": 1},
        "C": {"B": 3, "D": 5},
        "D": {}
    }
    print(f"    graph['A'] = {graph['A']}")
    print(f"    graph['A']['B'] = {graph['A']['B']}  (cost from A to B)")
    print(f"    graph['A'].items() = {list(graph['A'].items())}  (all neighbors with costs)")


def priority_queue_intro() -> None:
    """Introduce priority queues with heapq."""
    print_header("PRIORITY QUEUES (heapq)")
    
    print("""
    Dijkstra needs to always process the node with LOWEST cost first.
    A priority queue does this efficiently!
    
    C++:   std::priority_queue
    Java:  PriorityQueue
    Python: heapq module
    
    PYTHON heapq:
    -------------
    import heapq
    
    # Create a min-heap (smallest first)
    pq = []
    
    # Add items: heappush(heap, (priority, item))
    heapq.heappush(pq, (5, "node_A"))   # priority 5
    heapq.heappush(pq, (2, "node_B"))   # priority 2
    heapq.heappush(pq, (8, "node_C"))   # priority 8
    
    # Pop smallest: heappop(heap)
    cost, node = heapq.heappop(pq)  # Returns (2, "node_B")
    
    NOTE: heapq is a MIN-heap (smallest first)
    This is perfect for Dijkstra - we want lowest cost first!
    """)
    
    # Live demo
    print("LIVE DEMO:")
    pq = []
    heapq.heappush(pq, (5, "A"))
    print(f"    heappush(pq, (5, 'A'))  → pq = {pq}")
    heapq.heappush(pq, (2, "B"))
    print(f"    heappush(pq, (2, 'B'))  → pq = {pq}")
    heapq.heappush(pq, (8, "C"))
    print(f"    heappush(pq, (8, 'C'))  → pq = {pq}")
    item = heapq.heappop(pq)
    print(f"    heappop(pq)  → {item}  (smallest first!)")
    print(f"    pq now = {pq}")


def dijkstra_algorithm() -> None:
    """Explain Dijkstra's algorithm."""
    print_header("DIJKSTRA'S ALGORITHM")
    
    print("""
    ALGORITHM:
    
    1. Initialize:
       - costs = {start: 0, all others: infinity}
       - parents = {} (to reconstruct path)
       - priority_queue = [(0, start)]
    
    2. While priority queue not empty:
       a. Pop node with lowest cost
       b. If it's the destination, we're done!
       c. If we've already processed this node, skip it
       d. For each neighbor:
          - Calculate new_cost = current_cost + edge_weight
          - If new_cost < known cost to neighbor:
            - Update costs[neighbor] = new_cost
            - Update parents[neighbor] = current_node
            - Add (new_cost, neighbor) to priority queue
    
    3. Reconstruct path using parents dictionary
    
    EXAMPLE:
    --------
        A --6-- B --1-- D
        |       |
        2       3
        |       |
        C --5---+
    
    Find shortest path from A to D:
    
    Step 1: Start at A (cost 0)
            Neighbors: B (cost 6), C (cost 2)
            
    Step 2: Process C (lowest cost = 2)
            Neighbors: B (2+3=5), D (2+5=7)
            Update: B now costs 5 (better than 6!)
            
    Step 3: Process B (cost 5)
            Neighbors: D (5+1=6)
            Update: D now costs 6 (better than 7!)
            
    Step 4: Process D (cost 6) - destination reached!
    
    Path: A → C → B → D (total cost: 6)
    """)


def demo_dijkstra() -> None:
    """Demonstrate Dijkstra's algorithm."""
    print_header("TESTING DIJKSTRA")
    
    graph = {
        "A": {"B": 6, "C": 2},
        "B": {"D": 1},
        "C": {"B": 3, "D": 5},
        "D": {}
    }
    
    print("Graph:")
    print("    A --6-- B --1-- D")
    print("    |       |")
    print("    2       3")
    print("    |       |")
    print("    C --5---+")
    print()
    
    test_cases = [
        ("A", "D", 6, ["A", "C", "B", "D"]),
        ("A", "B", 5, ["A", "C", "B"]),
        ("A", "C", 2, ["A", "C"]),
        ("A", "A", 0, ["A"]),
    ]
    
    for start, end, expected_cost, expected_path in test_cases:
        print(f"dijkstra(graph, '{start}', '{end}'):")
        try:
            cost, path = dijkstra(graph, start, end)
            
            if cost == expected_cost:
                print(f"    Cost: {cost} ✅")
            elif cost is None:
                print(f"    Cost: None ❌ (expected {expected_cost})")
            else:
                print(f"    Cost: {cost} ❌ (expected {expected_cost})")
            
            if path == expected_path:
                print(f"    Path: {path} ✅")
            elif path is None or path == []:
                print(f"    Path: {path} ❌ (expected {expected_path})")
            else:
                # Path might be different but still valid
                print(f"    Path: {path}")
                if len(path) == len(expected_path):
                    print(f"    (Different path, same length - may be valid)")
                    
        except Exception as e:
            print(f"    ❌ Error: {e}")
        print()


def infinity_in_python() -> None:
    """Explain infinity in Python."""
    print_header("INFINITY IN PYTHON")
    
    print("""
    Dijkstra needs "infinity" for initial costs.
    
    PYTHON INFINITY:
    ----------------
    infinity = float('inf')
    
    # Comparisons work as expected
    float('inf') > 1000000000  # True
    float('inf') + 1           # Still infinity
    5 < float('inf')           # True
    
    USAGE IN DIJKSTRA:
    ------------------
    costs = {}
    costs[start] = 0
    
    # For any other node, cost is infinity until we find a path
    cost_to_node = costs.get(node, float('inf'))
    
    # Check if we found a better path
    if new_cost < costs.get(neighbor, float('inf')):
        costs[neighbor] = new_cost
    """)


def main():
    """Main entry point."""
    print("\n" + "🛤️" * 30)
    print("   LAB 09: DIJKSTRA'S ALGORITHM")
    print("   Shortest Paths in Weighted Graphs!")
    print("🛤️" * 30)
    
    print("""
    📋 YOUR TASKS:
    1. Open dijkstra.py
    2. Implement these functions:
       - dijkstra() - Main algorithm
       - build_path() - Reconstruct path from parents
    3. Run this file to test: python main.py
    4. Run pytest when ready: python -m pytest tests/ -v
    """)
    
    weighted_graphs_intro()
    priority_queue_intro()
    dijkstra_algorithm()
    infinity_in_python()
    demo_dijkstra()
    
    print_header("NEXT STEPS")
    print("""
    When all tests pass, run: python -m pytest tests/ -v
    Then complete the Lab Report in README.md
    """)


if __name__ == "__main__":
    main()
