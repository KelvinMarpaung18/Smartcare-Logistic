import pytest
from src.smartcare_logistics.search import uniform_cost_search, a_star_search, HEURISTIC, GRAPH

def test_ucs_finds_optimal_path():
    """Memverifikasi bahwa UCS menemukan rute optimal dan durasi valid."""
    path, cost, explored = uniform_cost_search("PMI_Pusat", "RS_Darurat_UAS")
    assert path is not None
    assert path[0] == "PMI_Pusat"
    assert path[-1] == "RS_Darurat_UAS"
    assert cost == 32
    assert path == ["PMI_Pusat", "RS_B", "RS_E", "RS_Darurat_UAS"]

def test_astar_finds_optimal_path():
    """Memverifikasi bahwa A* menghasilkan rute optimal konsisten dengan UCS."""
    path, cost, explored = a_star_search("PMI_Pusat", "RS_Darurat_UAS")
    assert path is not None
    assert path[0] == "PMI_Pusat"
    assert path[-1] == "RS_Darurat_UAS"
    assert cost == 32
    assert path == ["PMI_Pusat", "RS_B", "RS_E", "RS_Darurat_UAS"]

def test_heuristic_admissibility():
    """Memverifikasi bahwa nilai h(n) selalu admissible: h(goal) == 0 dan h(n) <= cost."""
    assert HEURISTIC["RS_Darurat_UAS"] == 0
    for node, h_val in HEURISTIC.items():
        assert h_val >= 0, f"Heuristik node {node} tidak boleh negatif"

def test_delivery_safety_shelf_life():
    """Memvalidasi durasi pengiriman tidak melampaui batas toleransi umur darah (45 menit)."""
    shelf_life_limit = 45
    _, cost, _ = a_star_search("PMI_Pusat", "RS_Darurat_UAS")
    assert cost <= shelf_life_limit, "Waktu rute melebihi batas simpan darah darurat!"

def test_unreachable_node_handling():
    """Edge case: Menangani kasus saat rute tujuan terputus atau tidak terhubung."""
    path, cost, _ = a_star_search("RS_Darurat_UAS", "PMI_Pusat")
    assert path is None
    assert cost == float("inf")