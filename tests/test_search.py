import sys
import os

# Add src to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from smartcare_logistics.search import GRAPH, HEURISTIC, uniform_cost_search, a_star_search


def test_ucs_optimal_path():
    """Verify UCS returns an optimal route and exact minimum path cost of 32.0 minutes."""
    path, cost, nodes_explored = uniform_cost_search(GRAPH, "PMI_Pusat", "RS_Darurat_UAS")
    assert path is not None
    assert path[0] == "PMI_Pusat"
    assert path[-1] == "RS_Darurat_UAS"
    assert cost == 32.0
    calculated_cost = 0.0
    for i in range(len(path) - 1):
        calculated_cost += GRAPH[path[i]][path[i+1]]
    assert calculated_cost == 32.0


def test_astar_search_optimal_path():
    """Verify A* search returns the optimal path equal in cost to UCS."""
    ucs_path, ucs_cost, _ = uniform_cost_search(GRAPH, "PMI_Pusat", "RS_Darurat_UAS")
    astar_path, astar_cost, _ = a_star_search(GRAPH, "PMI_Pusat", "RS_Darurat_UAS", HEURISTIC)
    
    assert astar_path is not None
    assert astar_cost == ucs_cost
    assert astar_path == ucs_path


def test_astar_efficiency():
    """Verify A* search explores fewer or equal nodes compared to uninformed UCS."""
    _, _, ucs_explored = uniform_cost_search(GRAPH, "PMI_Pusat", "RS_Darurat_UAS")
    _, _, astar_explored = a_star_search(GRAPH, "PMI_Pusat", "RS_Darurat_UAS", HEURISTIC)
    
    assert astar_explored <= ucs_explored


def test_heuristic_admissibility():
    """Verify that heuristic h(n) <= true minimum cost h*(n) for all nodes."""
    goal = "RS_Darurat_UAS"
    for node in GRAPH:
        _, true_cost, _ = uniform_cost_search(GRAPH, node, goal)
        h_val = HEURISTIC.get(node, 0.0)
        assert h_val <= true_cost, f"Heuristic overestimates at node {node}: {h_val} > {true_cost}"


def test_delivery_safety_margin():
    """Verify estimated delivery time is within cold chain shelf life limit (45 minutes)."""
    shelf_life_limit = 45.0
    _, astar_cost, _ = a_star_search(GRAPH, "PMI_Pusat", "RS_Darurat_UAS", HEURISTIC)
    assert astar_cost <= shelf_life_limit


def test_edge_case_unreachable_node():
    """Verify search returns None and infinity cost when no path exists."""
    disconnected_graph = {
        "Node_A": {"Node_B": 5.0},
        "Node_B": {},
        "Isolated_Node": {}
    }
    path, cost, _ = uniform_cost_search(disconnected_graph, "Node_A", "Isolated_Node")
    assert path is None
    assert cost == float("inf")


def test_edge_case_start_is_goal():
    """Verify search handles scenario where start node is the goal node."""
    path, cost, _ = uniform_cost_search(GRAPH, "PMI_Pusat", "PMI_Pusat")
    assert path == ["PMI_Pusat"]
    assert cost == 0.0