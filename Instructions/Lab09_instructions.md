# Lab 9: Dijkstra's Algorithm

## 1. Introduction and Objectives

### Overview
Implement Dijkstra's algorithm to find the shortest weighted path between Texas cities. Unlike BFS (Lab 6), Dijkstra's handles roads with different distances.

### Learning Objectives
- Understand weighted graphs
- Implement Dijkstra's algorithm with priority queue
- Compare BFS shortest path vs Dijkstra's shortest path
- Analyze algorithm performance

### Prerequisites
- Complete Labs 1-8
- Read Chapter 9 in "Grokking Algorithms" (pages 163-186)

---

## 2. Algorithm Background

### BFS vs Dijkstra's
| Algorithm | Graph Type | Finds | Example |
|-----------|------------|-------|---------|
| BFS | Unweighted | Fewest edges | Fewest stops |
| Dijkstra's | Weighted (positive) | Lowest total weight | Shortest distance |

### Key Insight
BFS finds path with fewest edges, but that's not always shortest distance!

```
Houston ----100mi---- Austin ----80mi---- Dallas
Houston ----250mi------------------------ Dallas

BFS: Houston → Dallas (1 edge)
Dijkstra's: Houston → Austin → Dallas (180mi < 250mi)
```

### Dijkstra's Algorithm Steps
1. Start at source, distance = 0
2. Mark all other distances as infinity
3. Visit unvisited node with smallest distance
4. Update neighbors' distances if shorter path found
5. Repeat until destination reached

### Time Complexity
- With array: O(V²)
- With binary heap: O((V + E) log V)
- With Fibonacci heap: O(E + V log V)

### Limitation
**Does NOT work with negative edge weights!**
(Use Bellman-Ford for negative weights)

---

## 3. Project Structure

```
lab09_dijkstra/
├── weighted_graph.py  # Weighted graph implementation
├── dijkstra.py        # Dijkstra's algorithm
├── main.py            # Main program
└── README.md          # Your lab report
```

---

## 4. Step-by-Step Implementation

### Step 1: Create `weighted_graph.py`

```python
"""
Lab 9: Weighted Graph Implementation
Texas highway network with actual distances.
"""
from typing import Dict, List, Tuple, Set
from collections import defaultdict


class WeightedGraph:
    """
    Weighted undirected graph using adjacency list.
    
    Each edge has a weight (distance in miles).
    Adjacency list stores: vertex -> [(neighbor, weight), ...]
    """
    
    def __init__(self):
        self.adjacency_list: Dict[str, List[Tuple[str, int]]] = defaultdict(list)
        self.vertices: Set[str] = set()
    
    def add_vertex(self, vertex: str) -> None:
        """Add a vertex to the graph."""
        self.vertices.add(vertex)
    
    def add_edge(self, v1: str, v2: str, weight: int) -> None:
        """
        Add weighted undirected edge between v1 and v2.
        Weight represents distance in miles.
        """
        self.vertices.add(v1)
        self.vertices.add(v2)
        
        # Check if edge already exists
        for neighbor, w in self.adjacency_list[v1]:
            if neighbor == v2:
                return  # Edge exists
        
        # Undirected: add both directions
        self.adjacency_list[v1].append((v2, weight))
        self.adjacency_list[v2].append((v1, weight))
    
    def get_neighbors(self, vertex: str) -> List[Tuple[str, int]]:
        """Get all neighbors with edge weights."""
        return self.adjacency_list[vertex]
    
    def get_edge_weight(self, v1: str, v2: str) -> int:
        """Get weight of edge between v1 and v2."""
        for neighbor, weight in self.adjacency_list[v1]:
            if neighbor == v2:
                return weight
        return float('inf')  # No edge
    
    def display(self) -> None:
        """Display the weighted graph."""
        print("\nWeighted Graph (Texas Highway Network):")
        print("-" * 50)
        for vertex in sorted(self.vertices):
            neighbors = self.adjacency_list[vertex]
            edges = [f"{n}({w}mi)" for n, w in sorted(neighbors)]
            print(f"{vertex}: {', '.join(edges)}")
    
    def __len__(self) -> int:
        return len(self.vertices)


def create_texas_highway_network() -> WeightedGraph:
    """
    Create Texas highway network with actual approximate distances.
    Distances are in miles (approximate highway distances).
    """
    g = WeightedGraph()
    
    # Highway connections with distances (miles)
    highways = [
        # I-45: Houston - Dallas corridor
        ("Houston", "Dallas", 240),
        
        # I-35: Dallas - Austin - San Antonio - Laredo
        ("Dallas", "Austin", 195),
        ("Austin", "San Antonio", 80),
        ("San Antonio", "Laredo", 155),
        
        # I-10: Houston - San Antonio - El Paso
        ("Houston", "San Antonio", 200),
        ("San Antonio", "El Paso", 550),
        
        # I-20: Dallas - Fort Worth - Lubbock - El Paso
        ("Dallas", "Fort Worth", 35),
        ("Fort Worth", "Lubbock", 320),
        ("Lubbock", "El Paso", 340),
        
        # Other major routes
        ("Dallas", "Arlington", 20),
        ("Fort Worth", "Arlington", 15),
        ("Houston", "Corpus Christi", 210),
        ("Corpus Christi", "San Antonio", 145),
        ("Austin", "Killeen", 70),
        ("Dallas", "Plano", 20),
        ("Dallas", "Irving", 15),
        ("Dallas", "Garland", 15),
        ("Plano", "Frisco", 15),
        ("Plano", "McKinney", 15),
        ("Corpus Christi", "Brownsville", 160),
        ("Brownsville", "McAllen", 60),
        ("McAllen", "Laredo", 145),
        ("Lubbock", "Amarillo", 125),
        ("Houston", "Pasadena", 15),
    ]
    
    for city1, city2, distance in highways:
        g.add_edge(city1, city2, distance)
    
    return g
```

### Step 2: Create `dijkstra.py`

```python
"""
Lab 9: Dijkstra's Algorithm Implementation
Finds shortest weighted path in graphs with positive weights.
"""
from typing import Dict, List, Tuple, Optional, Set
import heapq
from weighted_graph import WeightedGraph


def dijkstra(graph: WeightedGraph, start: str, end: str) -> Tuple[Optional[List[str]], int]:
    """
    Find shortest path from start to end using Dijkstra's algorithm.
    
    Uses a min-heap (priority queue) for efficiency.
    
    Time Complexity: O((V + E) log V) with binary heap
    Space Complexity: O(V)
    
    Returns:
        Tuple of (path as list of vertices, total distance)
        Returns (None, infinity) if no path exists
    """
    if start not in graph.vertices or end not in graph.vertices:
        print(f"Error: '{start}' or '{end}' not in graph")
        return None, float('inf')
    
    # Distance from start to each vertex (infinity initially)
    distances: Dict[str, float] = {v: float('inf') for v in graph.vertices}
    distances[start] = 0
    
    # Track the previous vertex in shortest path
    previous: Dict[str, Optional[str]] = {v: None for v in graph.vertices}
    
    # Priority queue: (distance, vertex)
    # Python's heapq is a min-heap
    pq: List[Tuple[int, str]] = [(0, start)]
    
    # Track visited vertices
    visited: Set[str] = set()
    
    print(f"\nDijkstra's Algorithm: {start} → {end}")
    print("-" * 50)
    
    while pq:
        # Get vertex with smallest distance
        current_dist, current = heapq.heappop(pq)
        
        # Skip if already visited (we found a shorter path earlier)
        if current in visited:
            continue
        
        visited.add(current)
        print(f"Visiting: {current} (distance from {start}: {current_dist} mi)")
        
        # Found destination!
        if current == end:
            path = _reconstruct_path(previous, start, end)
            print(f"\nFound shortest path: {current_dist} miles")
            return path, current_dist
        
        # Check all neighbors
        for neighbor, edge_weight in graph.get_neighbors(current):
            if neighbor in visited:
                continue
            
            # Calculate new distance through current vertex
            new_dist = current_dist + edge_weight
            
            # If shorter path found, update
            if new_dist < distances[neighbor]:
                old_dist = distances[neighbor]
                distances[neighbor] = new_dist
                previous[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))
                
                if old_dist == float('inf'):
                    print(f"  → {neighbor}: ∞ → {new_dist} mi (via {current})")
                else:
                    print(f"  → {neighbor}: {old_dist} → {new_dist} mi (shorter via {current})")
    
    print(f"\nNo path found from {start} to {end}")
    return None, float('inf')


def _reconstruct_path(previous: Dict[str, Optional[str]], start: str, end: str) -> List[str]:
    """Reconstruct path from previous pointers."""
    path = []
    current = end
    
    while current is not None:
        path.append(current)
        current = previous[current]
    
    path.reverse()
    return path


def dijkstra_all_destinations(graph: WeightedGraph, start: str) -> Dict[str, Tuple[int, List[str]]]:
    """
    Find shortest paths from start to ALL other vertices.
    
    Returns:
        Dict mapping vertex -> (distance, path)
    """
    if start not in graph.vertices:
        return {}
    
    distances: Dict[str, float] = {v: float('inf') for v in graph.vertices}
    distances[start] = 0
    
    previous: Dict[str, Optional[str]] = {v: None for v in graph.vertices}
    
    pq: List[Tuple[int, str]] = [(0, start)]
    visited: Set[str] = set()
    
    while pq:
        current_dist, current = heapq.heappop(pq)
        
        if current in visited:
            continue
        
        visited.add(current)
        
        for neighbor, edge_weight in graph.get_neighbors(current):
            if neighbor in visited:
                continue
            
            new_dist = current_dist + edge_weight
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))
    
    # Build result with paths
    result = {}
    for vertex in graph.vertices:
        if distances[vertex] < float('inf'):
            path = []
            current = vertex
            while current is not None:
                path.append(current)
                current = previous[current]
            path.reverse()
            result[vertex] = (int(distances[vertex]), path)
    
    return result


def compare_bfs_vs_dijkstra(graph: WeightedGraph, start: str, end: str) -> None:
    """
    Compare BFS (fewest edges) vs Dijkstra's (shortest distance).
    """
    from collections import deque
    
    print(f"\n{'=' * 50}")
    print(f"BFS vs DIJKSTRA: {start} → {end}")
    print("=" * 50)
    
    # BFS: Find path with fewest edges
    queue = deque([(start, [start])])
    visited = {start}
    bfs_path = None
    
    while queue and bfs_path is None:
        current, path = queue.popleft()
        
        if current == end:
            bfs_path = path
            break
        
        for neighbor, _ in graph.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    # Calculate BFS path distance
    bfs_distance = 0
    if bfs_path:
        for i in range(len(bfs_path) - 1):
            bfs_distance += graph.get_edge_weight(bfs_path[i], bfs_path[i + 1])
    
    # Dijkstra's: Find shortest distance path
    dijkstra_path, dijkstra_distance = dijkstra(graph, start, end)
    
    # Compare results
    print(f"\n{'=' * 50}")
    print("COMPARISON RESULTS")
    print("=" * 50)
    
    print(f"\nBFS (fewest edges):")
    print(f"  Path: {' → '.join(bfs_path)}")
    print(f"  Edges: {len(bfs_path) - 1}")
    print(f"  Total distance: {bfs_distance} miles")
    
    print(f"\nDijkstra's (shortest distance):")
    print(f"  Path: {' → '.join(dijkstra_path)}")
    print(f"  Edges: {len(dijkstra_path) - 1}")
    print(f"  Total distance: {dijkstra_distance} miles")
    
    if bfs_distance > dijkstra_distance:
        savings = bfs_distance - dijkstra_distance
        print(f"\n✓ Dijkstra's saves {savings} miles!")
    elif bfs_distance == dijkstra_distance:
        print(f"\n= Both paths have same distance")
    else:
        print(f"\n! BFS found shorter distance (unusual)")
```

### Step 3: Create `main.py`

```python
"""
Lab 9: Main Program
Demonstrates Dijkstra's algorithm on Texas highway network.
"""
from weighted_graph import WeightedGraph, create_texas_highway_network
from dijkstra import dijkstra, dijkstra_all_destinations, compare_bfs_vs_dijkstra


def main():
    # =========================================
    # PART 1: Create Weighted Graph
    # =========================================
    print("=" * 60)
    print("PART 1: TEXAS HIGHWAY NETWORK (WEIGHTED GRAPH)")
    print("=" * 60)
    
    highways = create_texas_highway_network()
    print(f"\nCreated network with {len(highways)} cities")
    highways.display()
    
    # =========================================
    # PART 2: Dijkstra's Algorithm
    # =========================================
    print("\n" + "=" * 60)
    print("PART 2: DIJKSTRA'S SHORTEST PATH")
    print("=" * 60)
    
    # Houston to El Paso
    path, distance = dijkstra(highways, "Houston", "El Paso")
    if path:
        print(f"\nRoute: {' → '.join(path)}")
        print(f"Total: {distance} miles")
    
    # Houston to Amarillo
    print("\n" + "-" * 50)
    path, distance = dijkstra(highways, "Houston", "Amarillo")
    if path:
        print(f"\nRoute: {' → '.join(path)}")
        print(f"Total: {distance} miles")
    
    # =========================================
    # PART 3: BFS vs Dijkstra Comparison
    # =========================================
    print("\n" + "=" * 60)
    print("PART 3: BFS vs DIJKSTRA COMPARISON")
    print("=" * 60)
    
    # This shows why Dijkstra's is needed for weighted graphs
    compare_bfs_vs_dijkstra(highways, "Houston", "El Paso")
    
    # =========================================
    # PART 4: All Destinations from Houston
    # =========================================
    print("\n" + "=" * 60)
    print("PART 4: ALL DISTANCES FROM HOUSTON")
    print("=" * 60)
    
    all_paths = dijkstra_all_destinations(highways, "Houston")
    
    # Sort by distance
    sorted_destinations = sorted(all_paths.items(), key=lambda x: x[1][0])
    
    print("\nCities by distance from Houston:")
    print("-" * 50)
    for city, (distance, path) in sorted_destinations:
        if city != "Houston":
            print(f"{city:15} {distance:4} mi  ({len(path)-1} stops)")
    
    # =========================================
    # PART 5: Key Concepts
    # =========================================
    print("\n" + "=" * 60)
    print("PART 5: KEY CONCEPTS")
    print("=" * 60)
    print("""
    DIJKSTRA'S ALGORITHM:
    
    1. GREEDY APPROACH
       - Always process vertex with smallest known distance
       - Once visited, distance is final (for positive weights)
    
    2. RELAXATION
       - For each neighbor, check if going through current
         vertex gives a shorter path
       - If yes, update distance and previous pointer
    
    3. PRIORITY QUEUE
       - Efficiently get minimum distance vertex
       - Binary heap: O(log V) for insert/extract-min
    
    4. WHY IT WORKS
       - Positive weights guarantee: once we visit a vertex,
         we've found the shortest path to it
       - We always process closest unvisited vertex first
    
    LIMITATIONS:
    - Does NOT work with negative edge weights!
    - For negative weights, use Bellman-Ford algorithm
    
    TIME COMPLEXITY:
    - With array: O(V²)
    - With binary heap: O((V + E) log V)
    - With Fibonacci heap: O(E + V log V)
    
    APPLICATIONS:
    - GPS navigation
    - Network routing (OSPF protocol)
    - Social networks (degrees of separation)
    - Game AI pathfinding
    """)


if __name__ == "__main__":
    main()
```

---

## 5. Lab Report Template

```markdown
# Lab 9: Dijkstra's Algorithm

## Student Information
- **Name:** [Your Name]
- **Date:** [Date]

## Algorithm Concepts

### BFS vs Dijkstra's
| Aspect | BFS | Dijkstra's |
|--------|-----|------------|
| Graph type | | |
| Finds | | |
| Data structure | | |
| Time complexity | | |

### Relaxation Process
[Explain how Dijkstra's updates distances]

## Test Results

### Houston to El Paso
- Path: 
- Distance:
- Number of stops:

### BFS vs Dijkstra Comparison
| Metric | BFS Path | Dijkstra Path |
|--------|----------|---------------|
| Route | | |
| Edges | | |
| Distance | | |

## Distance Table from Houston

| City | Distance (mi) | Stops |
|------|---------------|-------|
| | | |
| | | |
| | | |

## Reflection Questions

1. Why doesn't Dijkstra's work with negative edge weights?

2. Why do we use a priority queue instead of a regular queue?

3. Give a real-world example where BFS would give wrong answer but Dijkstra's would be correct.

4. What is "relaxation" in Dijkstra's algorithm?
```

---

## 6. Submission
Save files in `lab09_dijkstra/`, complete README, commit and push.
