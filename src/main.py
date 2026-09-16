import heapq

# 1. Ruang Keadaan (Graph Jaringan RS & Bank Darah)
# Node: Lokasi, Edge: Waktu Tempuh / Biaya Jalan (dalam menit)
GRAPH = {
    'PMI_Pusat': {'RS_A': 10, 'RS_B': 15},
    'RS_A': {'PMI_Pusat': 10, 'RS_C': 12, 'RS_D': 15},
    'RS_B': {'PMI_Pusat': 15, 'RS_D': 10, 'RS_E': 20},
    'RS_C': {'RS_A': 12, 'RS_D': 5, 'RS_Darurat_UAS': 10},
    'RS_D': {'RS_A': 15, 'RS_B': 10, 'RS_C': 5, 'RS_Darurat_UAS': 8},
    'RS_E': {'RS_B': 20, 'RS_Darurat_UAS': 5},
    'RS_Darurat_UAS': {'RS_C': 10, 'RS_D': 8, 'RS_E': 5}
}

# 2. Heuristik Admissible (Estimasi Jarak Garis Lurus / Manhattan ke Tujuan)
HEURISTIC = {
    'PMI_Pusat': 22,
    'RS_A': 14,
    'RS_B': 12,
    'RS_C': 8,
    'RS_D': 6,
    'RS_E': 4,
    'RS_Darurat_UAS': 0
}

def a_star_search(graph, start, goal, heuristic):
    """
    Algoritma A* Search untuk optimasi rute distribusi darah darurat.
    Priority Queue menyimpan tuple: (f_score, cost_g, current_node, path)
    """
    pq = [(heuristic[start], 0, start, [start])]
    visited = {}

    while pq:
        f_score, g_score, current, path = heapq.heappop(pq)

        if current == goal:
            return path, g_score

        if current in visited and visited[current] <= g_score:
            continue
        visited[current] = g_score

        for neighbor, weight in graph.get(current, {}).items():
            new_g = g_score + weight
            new_f = new_g + heuristic.get(neighbor, 0)
            if neighbor not in visited or new_g < visited[neighbor]:
                heapq.heappush(pq, (new_f, new_g, neighbor, path + [neighbor]))

    return None, float('inf')

if __name__ == "__main__":
    start_node = 'PMI_Pusat'
    target_node = 'RS_Darurat_UAS'
    
    path, total_cost = a_star_search(GRAPH, start_node, target_node, HEURISTIC)
    print(f"Rute Optimal Darurat : {' -> '.join(path)}")
    print(f"Total Waktu Tempuh  : {total_cost} Menit")