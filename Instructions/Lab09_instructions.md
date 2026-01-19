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

## Your Tasks

### Task 1: Implement `dijkstra()`
Find shortest path from start to end:
- Initialize costs: start=0, others=infinity (`float('inf')`)
- Track parents to reconstruct path
- Use a priority queue (heapq) for efficiency
- Process nodes in order of lowest cost
- Update costs when you find a shorter path
- Return `(total_cost, path)` or `(None, [])` if no path

### Task 2: Implement `build_path()`
Reconstruct the path from parents dictionary:
- Start at end node
- Follow parent pointers back to start
- Reverse to get path from start to end

## Example

```python
graph = {
    "a": {"b": 6, "c": 2},
    "b": {"d": 1},
    "c": {"b": 3, "d": 5},
    "d": {}
}

>>> dijkstra(graph, "a", "d")
(6, ['a', 'c', 'b', 'd'])

# Paths considered:
# a→b→d = 6+1 = 7
# a→c→d = 2+5 = 7
# a→c→b→d = 2+3+1 = 6  ← shortest!
```

## Testing
```bash
python -m pytest tests/ -v
```

## Hints
- Use `heapq` for the priority queue:
  ```python
  import heapq
  heapq.heappush(queue, (cost, node))
  cost, node = heapq.heappop(queue)
  ```
- Use `float('inf')` for infinity
- Skip nodes you've already processed (they have optimal cost)
- Store `parents[neighbor] = current_node` when updating costs

## Common Mistakes
- Forgetting to skip already-processed nodes
- Not handling the case where end is unreachable
- Using a regular list instead of heapq (slower)

## Submission
Commit and push your completed `dijkstra.py` file.
