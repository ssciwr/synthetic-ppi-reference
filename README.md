# synthetic-ppi-reference

Reference solution for the model evaluation of the BioCypher agentic workspace of [biocypher-components-registry](https://github.com/ssciwr/biocypher-components-registry); the evaluation harness and its design (`docs/evaluating_models_workspace.md`) are in the [biocypher-workspace-eval](https://github.com/ssciwr/biocypher-workspace-eval) repository.

It is the BioCypher adapter project that a model in the workspace is asked to build: a project generated from the [BioCypher cookiecutter template](https://github.com/biocypher/biocypher-cookiecutter-template), completed for the [Synthetic Protein Interaction Dataset](https://doi.org/10.5281/zenodo.21455347). The evaluation uses it to

- define and validate the grader: this solution must pass every check, and mutants derived from its adapter must each fail the expected check;
- provide the pristine scaffold for the levels that start from a scaffolded project (the first commit, see below).

## Contents

| Path | What |
|---|---|
| `src/synthetic_ppi/adapters/synthetic_ppi_adapter.py` | reference adapter `SyntheticPpiAdapter` |
| `config/schema_config.yaml` | schema: Biolink `protein` nodes, `pairwise molecular interaction` edges |
| `tests/` | adapter tests against the dataset, and an end-to-end graph build test |
| `data/` | the dataset, copied unchanged from Zenodo (see [data/README.md](data/README.md)) |

Expected result: 15 `Protein` nodes and 21 `PairwiseMolecularInteraction` edges. Data handling: gene symbols upper-cased; rows identical after that kept once (one exact duplicate, one hidden by `GAPDH`/`gapdh`); everything else kept as given (no reverse edges for the undirected row, contradictory flags unchanged, 0/1 flags as `bool`).

## Usage

Requires Python ≥ 3.13 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run pytest                          # adapter tests + graph build
uv run python create_knowledge_graph.py  # writes biocypher-out/*.parquet
```

The first run downloads the Biolink 3.2.1 ontology.

## Provenance

The first commit is the unmodified output of

```bash
cookiecutter https://github.com/biocypher/biocypher-cookiecutter-template.git \
  --checkout 01d32f162a88de433edfbe3cda3a4b7896145047 --no-input \
  project_name="synthetic-ppi" project_description="BioCypher project for the Synthetic Protein Interaction Dataset" \
  package_name="synthetic_ppi" adapter_name="synthetic_ppi_adapter" data_source_type="file" \
  include_docker="y" include_tests="y" schema_config="y" \
  author_name="BioCypher User" author_email="user@example.com" version="0.1.0"
```

(the template's post-generation hook runs `git init` and creates that commit). The arguments are the defaults that the BioCypher MCP's `get_cookiecutter_instructions` (server 1.13.1) prescribes. `git diff <first commit>` shows the complete solution. Changes to the scaffold, apart from the adapter, schema and tests:

| Scaffold defect | Fix |
|---|---|
| `pyarrow` missing, so `create_knowledge_graph.py` fails with `ModuleNotFoundError` (BioCypher 0.17 writes Parquet) | added to `pyproject.toml` |
| `create_knowledge_graph.py` points to `data/your_data.csv` | points to the dataset |
| example `get_edges()` yields tuples in the wrong order (`source, target, label, type, props`) | BioCypher order `(edge_id, source, target, label, props)` |
| template tests check the dummy implementation (pass on the empty scaffold, fail on a real adapter) | replaced by tests of the real adapter |
| `.gitignore` excludes `data/` | un-ignored for the pinned dataset |
| `pyproject.toml` URLs point to the placeholder `github.com/biocypher-user/synthetic_ppi` | point to this repository |

The remaining scaffold files (other `pyproject.toml` metadata, Docker files, `config/biocypher_config.yaml`) are left as generated so the diff stays minimal.

Verified with Python 3.13.12, BioCypher 0.17.0, pyarrow 26.0.0 (see `uv.lock`).

## Citation

See [CITATION.cff](CITATION.cff). If you use the dataset, cite it as given in [data/README.md](data/README.md).

## License

MIT, see [LICENSE](LICENSE). The dataset has its own MIT license ([data/README.md](data/README.md)).

---

*AI involvement in this project is declared in [aidecl.yaml](./aidecl.yaml) following the [AI Declaration Format](https://ai-declaration.org).*
