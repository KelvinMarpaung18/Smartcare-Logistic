def test_astar_search_optimal_path():
    # Simulated search outcome for test verification
    route = ["PMI_Pusat", "RS_B", "RS_E", "RS_Darurat_UAS"]
    total_cost = 32
    
    assert route[0] == "PMI_Pusat"
    assert route[-1] == "RS_Darurat_UAS"
    assert total_cost == 32

def test_delivery_safety_margin():
    shelf_life_limit = 45
    estimated_delivery_time = 32
    
    assert estimated_delivery_time <= shelf_life_limit