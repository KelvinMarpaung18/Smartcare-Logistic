import sys
from pathlib import Path

# Memasukkan folder 'src' ke dalam sistem path Python
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from main import a_star_search, GRAPH, HEURISTIC

def test_a_star_path_found():
    path, cost = a_star_search(GRAPH, 'PMI_Pusat', 'RS_Darurat_UAS', HEURISTIC)
    assert path is not None
    assert path[0] == 'PMI_Pusat'
    assert path[-1] == 'RS_Darurat_UAS'
    assert cost > 0

def test_a_star_optimal_cost():
    _, cost = a_star_search(GRAPH, 'PMI_Pusat', 'RS_Darurat_UAS', HEURISTIC)
    # Memastikan biaya waktu tempuh terhitung tepat
    assert cost == 32