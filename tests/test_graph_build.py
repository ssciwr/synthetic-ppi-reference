"""End-to-end: BioCypher writes the expected graph (needs network on first run
to fetch the Biolink ontology)."""

from pathlib import Path

import pyarrow.parquet as pq
from biocypher import BioCypher

from synthetic_ppi.adapters.synthetic_ppi_adapter import FLAGS, SyntheticPpiAdapter

ROOT = Path(__file__).parent.parent


def test_graph_build(tmp_path, monkeypatch):
    monkeypatch.chdir(ROOT)  # the BioCypher config uses relative paths
    bc = BioCypher(
        biocypher_config_path="config/biocypher_config.yaml",
        schema_config_path="config/schema_config.yaml",
        output_directory=str(tmp_path),
    )
    adapter = SyntheticPpiAdapter(data_source="data/synthetic_protein_interactions.tsv")
    bc.write_nodes(adapter.get_nodes())
    bc.write_edges(adapter.get_edges())

    proteins = pq.read_table(tmp_path / "Protein-part000.parquet")
    edges = pq.read_table(tmp_path / "PairwiseMolecularInteraction-part000.parquet")
    assert proteins.num_rows == 15
    assert edges.num_rows == 21
    for flag in FLAGS:
        assert str(edges.schema.field(flag).type) == "bool"
