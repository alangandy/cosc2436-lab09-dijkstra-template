# Lab 09: Dijkstra's Algorithm

## Overview
In this lab, you will implement **Dijkstra's Algorithm** from Chapter 9 of "Grokking Algorithms." Dijkstra's finds the shortest path in weighted graphs.

## Learning Objectives
- Understand weighted graphs
- Implement Dijkstra's shortest path algorithm
- Use priority queues for efficiency
- Understand when Dijkstra's works (and when it doesn't)

## Background

### Weighted Graphs
Unlike BFS (which treats all edges equally), weighted graphs have costs on edges:
```
    A ---6--- B
    |         |
    2         1
    |         |
    C ---3--- D
```
Shortest path A→D: A→C→D (cost 5), not A→B→D (cost 7)

### BFS vs Dijkstra's
- **BFS**: Finds shortest path by number of edges (unweighted)
- **Dijkstra's**: Finds shortest path by total weight (weighted)

### Dijkstra's Algorithm
1. Start with source node, cost = 0
2. Mark all other nodes as cost = infinity
3. While unvisited nodes remain:
   - Pick unvisited node with lowest cost
   - For each neighbor, calculate new cost through current node
   - If new cost < known cost, update it
4. Reconstruct path using parent pointers

### Important Limitation
Dijkstra's does NOT work with **negative edge weights**! Use Bellman-Ford for that.

---

## Complete Solutions

### Task 1: `dijkstra()` - Complete Implementation

```python
import heapq
from typing import Dict, List, Tuple, Optional

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
    """
    # Initialize costs: start=0, all others=infinity
    costs = {node: float('inf') for node in graph}
    costs[start] = 0
    
    # Track parents to reconstruct path
    parents = {start: None}
    
    # Track processed nodes
    processed = set()
    
    # Priority queue: (cost, node)
    heap = [(0, start)]
    
    while heap:
        # Get node with lowest cost
        current_cost, current_node = heapq.heappop(heap)
        
        # Skip if already processed (we found a better path earlier)
        if current_node in processed:
            continue
        
        # Mark as processed
        processed.add(current_node)
        
        # If we reached the end, reconstruct and return path
        if current_node == end:
            path = build_path(parents, start, end)
            return (costs[end], path)
        
        # Check all neighbors
        for neighbor, weight in graph.get(current_node, {}).items():
            if neighbor in processed:
                continue
            
            # Calculate new cost through current node
            new_cost = costs[current_node] + weight
            
            # If this path is better, update
            if new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                parents[neighbor] = current_node
                heapq.heappush(heap, (new_cost, neighbor))
    
    # No path found
    return (None, [])


def build_path(parents: Dict[str, str], start: str, end: str) -> List[str]:
    """Reconstruct path from parents dictionary."""
    path = []
    current = end
    
    while current is not None:
        path.append(current)
        current = parents.get(current)
    
    # Reverse to get path from start to end
    path.reverse()
    return path
```

---

## How It Works

### Step-by-step for `dijkstra()`:

1. **Initialize costs**: Set start node cost to 0, all others to infinity
2. **Initialize parents**: Dictionary to track the path
3. **Initialize processed set**: Track nodes we've finalized
4. **Initialize priority queue**: Start with (0, start_node)

5. **Main loop** (while heap is not empty):
   - Pop the node with lowest cost from the heap
   - If already processed, skip it (we found a better path)
   - Mark as processed
   - If it's the end node, reconstruct and return the path
   - For each neighbor:
     - Skip if already processed
     - Calculate new cost: `current_cost + edge_weight`
     - If new cost < known cost:
       - Update the cost
       - Update the parent
       - Add to heap with new cost

6. **If loop ends without finding end**: Return `(None, [])`

### `build_path()`:
1. Start at the end node
2. Follow parent pointers back to start
3. Reverse the list to get path from start to end

---

## Example Usage

```python
graph = {
    "a": {"b": 6, "c": 2},
    "b": {"d": 1},
    "c": {"b": 3, "d": 5},
    "d": {}
}

>>> dijkstra(graph, "a", "d")
(6, ['a', 'c', 'b', 'd'])

# Step-by-step execution:
# 
# Initial: costs = {a:0, b:inf, c:inf, d:inf}
# 
# Process 'a' (cost 0):
#   - neighbor 'b': new_cost = 0+6 = 6 < inf → update costs[b]=6, parents[b]='a'
#   - neighbor 'c': new_cost = 0+2 = 2 < inf → update costs[c]=2, parents[c]='a'
#   - heap: [(2,'c'), (6,'b')]
# 
# Process 'c' (cost 2):
#   - neighbor 'b': new_cost = 2+3 = 5 < 6 → update costs[b]=5, parents[b]='c'
#   - neighbor 'd': new_cost = 2+5 = 7 < inf → update costs[d]=7, parents[d]='c'
#   - heap: [(5,'b'), (6,'b'), (7,'d')]
# 
# Process 'b' (cost 5):
#   - neighbor 'd': new_cost = 5+1 = 6 < 7 → update costs[d]=6, parents[d]='b'
#   - heap: [(6,'b'), (6,'d'), (7,'d')]
# 
# Process 'b' (cost 6): already processed, skip
# 
# Process 'd' (cost 6): this is the end!
#   - path = build_path(parents, 'a', 'd') = ['a', 'c', 'b', 'd']
#   - return (6, ['a', 'c', 'b', 'd'])

# Another example - no path exists
graph2 = {
    "a": {"b": 1},
    "b": {},
    "c": {}
}
>>> dijkstra(graph2, "a", "c")
(None, [])
```

---

## Testing
```bash
python -m pytest tests/ -v
```

## Submission
Commit and push your completed `dijkstra.py` file.
