import time
import os
import sys

# Add src directory to sys.path if needed
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from smartcare_logistics.search import GRAPH, HEURISTIC, uniform_cost_search, a_star_search


def print_header():
    print("=" * 68)
    print(" [SMARTCARE LOGISTICS] ENTERPRISE EMERGENCY ROUTE COPILOT")
    print("=" * 68)
    print(" Dispatch ID   : DISP-2026-MED0918")
    print(" Cargo Type    : Emergency Blood Supply (Type O- & A+)")
    print(" Temp Control  : Cold Chain Monitored (2 deg C - 6 deg C)")
    print(" Urgency Level : CRITICAL (Shelf Life Remaining: 45 Mins)")
    print(" Start Node    : PMI_Pusat")
    print(" Goal Node     : RS_Darurat_UAS")
    print("=" * 68 + "\n")


def run_simulation():
    print_header()
    
    start_node = "PMI_Pusat"
    goal_node = "RS_Darurat_UAS"

    print("[1/2] Executing Uniform Cost Search (UCS) Baseline...")
    time.sleep(0.3)
    ucs_route, ucs_cost, ucs_nodes_explored = uniform_cost_search(GRAPH, start_node, goal_node)
    
    if ucs_route:
        print(f"      -> Path Found     : {' -> '.join(ucs_route)}")
        print(f"      -> Total Duration : {ucs_cost:.1f} Minutes")
        print(f"      -> Nodes Explored : {ucs_nodes_explored}\n")
    else:
        print("      -> No path found!\n")

    print("[2/2] Executing Informed A* Search Algorithm (Heuristic Guided)...")
    time.sleep(0.3)
    astar_route, astar_cost, astar_nodes_explored = a_star_search(GRAPH, start_node, goal_node, HEURISTIC)
    
    if astar_route:
        print(f"      -> Path Found     : {' -> '.join(astar_route)}")
        print(f"      -> Total Duration : {astar_cost:.1f} Minutes")
        print(f"      -> Nodes Explored : {astar_nodes_explored}\n")
    else:
        print("      -> No path found!\n")

    print("-" * 68)
    print(" OPTIMIZATION COMPARISON SUMMARY")
    print("-" * 68)
    if astar_route and ucs_route:
        reduction_pct = ((ucs_nodes_explored - astar_nodes_explored) / ucs_nodes_explored) * 100.0 if ucs_nodes_explored > 0 else 0.0
        print(f"  * Algorithm Selected    : A* Search (Informed Heuristic)")
        print(f"  * Optimal Delivery Route: {' -> '.join(astar_route)}")
        print(f"  * Total Estimated Time  : {astar_cost:.1f} Minutes")
        print(f"  * Efficiency Gain       : Explored {ucs_nodes_explored - astar_nodes_explored} fewer nodes vs UCS ({reduction_pct:.1f}% search reduction)")
        safety_status = "PASSED (< 45 Mins Shelf Life Limit)" if astar_cost <= 45 else "FAILED (Exceeds Shelf Life)"
        print(f"  * Safety Threshold      : {safety_status}")
    print("-" * 68)
    print(" [STATUS] SUCCESS - ROUTE DISPATCHED TO MEDICAL DRIVER DASHBOARD\n")


if __name__ == "__main__":
    run_simulation()