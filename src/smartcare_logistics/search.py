import heapq
from typing import Dict, List, Tuple, Optional

# Definition of the State-Space Graph for Medical Emergency Distribution
# Nodes: Health Facilities / Supply Nodes
# Edges: Adjacency list with travel time in minutes as cost
GRAPH: Dict[str, Dict[str, float]] = {
    "PMI_Pusat": {"RS_A": 10.0, "RS_B": 5.0},
    "RS_A": {"RS_C": 12.0, "RS_D": 8.0},
    "RS_B": {"RS_C": 18.0, "RS_E": 15.0},
    "RS_C": {"RS_Darurat_UAS": 10.0},
    "RS_D": {"RS_Darurat_UAS": 14.0},
    "RS_E": {"RS_Darurat_UAS": 12.0},
    "RS_Darurat_UAS": {}
}

# Heuristic Function h(n): Estimated travel time to RS_Darurat_UAS
# Admissibility condition: h(n) <= h*(n) (true minimum cost to goal)
HEURISTIC: Dict[str, float] = {
    "PMI_Pusat": 30.0,
    "RS_A": 20.0,
    "RS_B": 26.0,
    "RS_C": 9.0,
    "RS_D": 13.0,
    "RS_E": 11.0,
    "RS_Darurat_UAS": 0.0
}


def uniform_cost_search(
    graph: Dict[str, Dict[str, float]], 
    start: str, 
    goal: str
) -> Tuple[Optional[List[str]], float, int]:
    """
    Uniform Cost Search (UCS) algorithm using a priority queue (heapq).
    Returns tuple of (optimal_path, total_cost, nodes_explored).
    """
    if start not in graph or goal not in graph:
        return None, float("inf"), 0

    pq: List[Tuple[float, str, List[str]]] = [(0.0, start, [start])]
    visited: Dict[str, float] = {}
    nodes_explored = 0

    while pq:
        cost, current, path = heapq.heappop(pq)

        if current in visited and visited[current] <= cost:
            continue
        visited[current] = cost
        nodes_explored += 1

        if current == goal:
            return path, cost, nodes_explored

        for neighbor, edge_cost in graph.get(current, {}).items():
            new_cost = cost + edge_cost
            if neighbor not in visited or new_cost < visited[neighbor]:
                heapq.heappush(pq, (new_cost, neighbor, path + [neighbor]))

    return None, float("inf"), nodes_explored


def a_star_search(
    graph: Dict[str, Dict[str, float]], 
    start: str, 
    goal: str, 
    heuristic: Dict[str, float]
) -> Tuple[Optional[List[str]], float, int]:
    """
    A* Search algorithm using priority queue (heapq) guided by admissible heuristic.
    Returns tuple of (optimal_path, total_cost, nodes_explored).
    """
    if start not in graph or goal not in graph:
        return None, float("inf"), 0

    initial_h = heuristic.get(start, 0.0)
    # Tuple format: (f_score, h_score, g_score, current, path)
    # Tie-breaking by h_score prefers nodes closer to goal when f_scores are equal
    pq: List[Tuple[float, float, float, str, List[str]]] = [(initial_h, initial_h, 0.0, start, [start])]
    visited: Dict[str, float] = {}
    nodes_explored = 0

    while pq:
        f_score, h_score, g_score, current, path = heapq.heappop(pq)

        if current in visited and visited[current] <= g_score:
            continue
        visited[current] = g_score
        nodes_explored += 1

        if current == goal:
            return path, g_score, nodes_explored

        for neighbor, edge_cost in graph.get(current, {}).items():
            new_g = g_score + edge_cost
            new_h = heuristic.get(neighbor, 0.0)
            new_f = new_g + new_h

            if neighbor not in visited or new_g < visited[neighbor]:
                heapq.heappush(pq, (new_f, new_h, new_g, neighbor, path + [neighbor]))

    return None, float("inf"), nodes_explored
