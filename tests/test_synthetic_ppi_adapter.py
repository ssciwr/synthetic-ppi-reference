"""Tests for SyntheticPpiAdapter against the published dataset (Zenodo 1.0.5).

Expected values were derived independently from the raw file: 23 rows,
15 proteins, 21 interactions after normalizing symbol case and deduplicating.
"""

from pathlib import Path

import pytest

from synthetic_ppi.adapters.synthetic_ppi_adapter import FLAGS, SyntheticPpiAdapter

DATA = Path(__file__).parent.parent / "data" / "synthetic_protein_interactions.tsv"


@pytest.fixture
def adapter():
    return SyntheticPpiAdapter(data_source=DATA)


@pytest.fixture
def nodes(adapter):
    return {node_id: (label, props) for node_id, label, props in adapter.get_nodes()}


@pytest.fixture
def edges(adapter):
    return {edge[0]: edge for edge in adapter.get_edges()}


def test_node_count_and_label(adapter, nodes):
    assert len(list(adapter.get_nodes())) == 15
    assert len(nodes) == 15
    assert {label for label, _ in nodes.values()} == {"protein"}


def test_node_properties(nodes):
    assert nodes["P08228"][1] == {"genesymbol": "SOD1", "ncbi_tax_id": 10090}
    assert nodes["Q63356"][1] == {"genesymbol": "NFKB1", "ncbi_tax_id": 10116}
    assert all(isinstance(p["ncbi_tax_id"], int) for _, p in nodes.values())


def test_gene_symbols_upper_cased(nodes):
    # The file spells P04406 both "GAPDH" and "gapdh".
    assert nodes["P04406"][1]["genesymbol"] == "GAPDH"
    assert all(p["genesymbol"].isupper() for _, p in nodes.values())


def test_edge_count_and_tuple_shape(adapter, edges):
    all_edges = list(adapter.get_edges())
    assert len(all_edges) == 21
    assert len(edges) == 21  # ids are unique
    for edge_id, source, target, label, props in all_edges:
        assert edge_id == f"{source}_{target}_{props['type']}"
        assert label == "protein_protein_interaction"


def test_exact_duplicate_kept_once(adapter):
    ids = [e[0] for e in adapter.get_edges()]
    assert ids.count("P04637_Q9JHW1_ubiquitination") == 1


def test_duplicate_hidden_by_case_kept_once(adapter):
    # MYC -> GAPDH and MYC -> gapdh are the same row after normalization.
    ids = [e[0] for e in adapter.get_edges()]
    assert ids.count("P01106_P04406_phosphorylation") == 1


def test_undirected_row_kept_as_given(edges):
    _, source, target, _, props = edges["P00533_P08228_binding"]
    assert (source, target) == ("P00533", "P08228")
    assert props["is_directed"] is False
    # The directed reverse row exists separately; no edges were added.
    assert edges["P08228_P00533_binding"][4]["is_directed"] is True


def test_contradictory_flags_unchanged(edges):
    props = edges["P00533_P08228_binding"][4]
    assert props["is_stimulation"] is True
    assert props["is_inhibition"] is True


def test_flags_are_bool(edges):
    for *_, props in edges.values():
        assert set(props) == {"type", *FLAGS}
        assert all(type(props[f]) is bool for f in FLAGS)


def test_generators_can_be_iterated_twice(adapter):
    assert list(adapter.get_nodes()) == list(adapter.get_nodes())
    assert list(adapter.get_edges()) == list(adapter.get_edges())
