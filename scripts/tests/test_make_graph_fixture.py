import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_output as co  # noqa: E402
import make_graph_fixture as mg  # noqa: E402


def page(tmp_path):
    return (tmp_path / "docs/codemap/html/relation-map.html").read_text(encoding="utf-8")


def test_generated_fixture_passes_the_checker(tmp_path):
    mg.build(12, 3, tmp_path)
    assert co.main([str(tmp_path), str(tmp_path / "docs/codemap")]) == 0


def test_fixture_scales(tmp_path):
    mg.build(600, 40, tmp_path)
    assert len(co.parse_graph_html(page(tmp_path))) == 600


def test_fixture_covers_kinds_hub_mutual_pair_and_same_named_folders(tmp_path):
    mg.build(40, 4, tmp_path)
    nodes = co.parse_graph_html(page(tmp_path))
    assert {n["kind"] for n in nodes} == {"source", "test", "unverified"}
    by_id = {n["id"]: n for n in nodes}
    assert "g3" in by_id["g2"]["uses"] and "g2" in by_id["g3"]["uses"]  # mutual pair (node 1 <-> node 2)
    used = sum(1 for n in nodes if "g1" in n["uses"])
    assert used >= 5  # node 0 is a hub
    assert {"a/utils", "b/utils"} <= {n["group"] for n in nodes}  # same folder name at different depths


def test_single_file_fixture_has_no_edges(tmp_path):
    mg.build(1, 1, tmp_path)
    nodes = co.parse_graph_html(page(tmp_path))
    assert len(nodes) == 1 and nodes[0]["uses"] == []
    assert co.main([str(tmp_path), str(tmp_path / "docs/codemap")]) == 0
