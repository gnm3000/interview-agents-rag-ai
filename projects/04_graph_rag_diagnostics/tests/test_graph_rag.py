from pathlib import Path

from answer.synthesizer import synthesize_answer
from ingest.build_graph import build_graph_from_files
from retrieval.hybrid import hybrid_search
from retrieval.vector import build_index
from reasoning.planner import plan_steps


def test_graph_build():
    data_path = Path(__file__).parents[1] / "data" / "sample.txt"
    graph = build_graph_from_files([data_path])
    assert "Project Atlas" in graph
    assert graph.has_edge("Project Atlas", "Project Orion")


def test_hybrid_search():
    index = build_index(["Atlas owner Alice", "Phoenix maintained by Bob"])
    graph = build_graph_from_files([Path(__file__).parents[1] / "data" / "sample.txt"])
    results = hybrid_search(index, graph, "owner", "Project Atlas")
    assert results


def test_planner_steps():
    steps = plan_steps("Who is the owner?")
    assert "synthesize" in steps


def test_synthesizer():
    answer = synthesize_answer("Q", ["Fact A"])
    assert "Fact A" in answer
