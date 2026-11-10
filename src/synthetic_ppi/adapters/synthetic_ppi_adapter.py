"""Reference adapter for the Synthetic Protein Interaction Dataset.

Ground truth for the agentic-workspace model evaluation in
biocypher-workspace-eval, https://github.com/ssciwr/biocypher-workspace-eval
(docs/evaluating_models_workspace.md).

Dataset: Carreño, E. (2026). Synthetic Protein Interaction Dataset (1.0.5).
Zenodo. https://doi.org/10.5281/zenodo.21455347 (MIT license)

Data handling (the evaluation's specification):
- gene symbols are upper-cased (the file has both GAPDH and gapdh);
- rows identical after that normalization are kept once (one exact
  duplicate, one duplicate hidden by symbol case);
- everything else is kept as given: no reverse edges for undirected rows,
  no changes to contradictory flags; 0/1 flags become bool.
"""

import csv
from collections.abc import Iterator
from pathlib import Path

FLAGS = (
    "is_directed",
    "is_stimulation",
    "is_inhibition",
    "consensus_direction",
    "consensus_stimulation",
    "consensus_inhibition",
)


class SyntheticPpiAdapter:
    """BioCypher adapter yielding protein nodes and interaction edges."""

    def __init__(self, data_source: str | Path, **kwargs):
        self.data_source = data_source
        self.config = kwargs

    def _rows(self) -> Iterator[dict[str, str]]:
        """Normalized, deduplicated rows; re-reads the file on every call."""
        seen = set()
        with open(self.data_source, newline="") as fh:
            for row in csv.DictReader(fh, delimiter="\t"):
                row = {k: v.strip() for k, v in row.items()}
                row["source_genesymbol"] = row["source_genesymbol"].upper()
                row["target_genesymbol"] = row["target_genesymbol"].upper()
                key = tuple(row.values())
                if key not in seen:
                    seen.add(key)
                    yield row

    def get_nodes(self) -> Iterator[tuple[str, str, dict]]:
        """Yield (accession, "protein", properties), one per distinct protein."""
        nodes = {}
        for row in self._rows():
            for side in ("source", "target"):
                nodes[row[side]] = {
                    "genesymbol": row[f"{side}_genesymbol"],
                    "ncbi_tax_id": int(row[f"ncbi_tax_id_{side}"]),
                }
        for node_id, props in nodes.items():
            yield node_id, "protein", props

    def get_edges(self) -> Iterator[tuple[str, str, str, str, dict]]:
        """Yield (edge_id, source, target, label, properties), one per row."""
        for row in self._rows():
            yield (
                f"{row['source']}_{row['target']}_{row['type']}",
                row["source"],
                row["target"],
                "protein_protein_interaction",
                {"type": row["type"], **{f: row[f] == "1" for f in FLAGS}},
            )
