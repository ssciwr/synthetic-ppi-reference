# synthetic-ppi

BioCypher project for the Synthetic Protein Interaction Dataset

## Overview

This BioCypher pipeline processes file data using the synthetic_ppi_adapter to create a knowledge graph.

## Features

- **Data Source**: file data processing
- **Adapter**: synthetic_ppi_adapter
- **Output**: Neo4j knowledge graph
- **Docker Support**: Containerized deployment
- **Testing**: Comprehensive test suite

## Installation

### Prerequisites

- Python 3.13 or higher
- Neo4j database (local or remote)

### Setup

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd synthetic-ppi
   ```

2. Install dependencies:
   ```bash
   pip install -e .
   ```

   Or using uv:
   ```bash
   uv sync
   ```

3. Implement `get_nodes()` and `get_edges()` in the adapter (they return dummy data until then) and configure your data source in `create_knowledge_graph.py`

4. Update the schema configuration in `config/schema_config.yaml` if needed

## Usage

### Basic Usage

Run the pipeline to create the knowledge graph:

```bash
python create_knowledge_graph.py
```

This writes the output files and `neo4j-admin-import-call.sh` to `biocypher-out/`. Run that script from your Neo4j home directory to import the data.

### Configuration

The pipeline uses two main configuration files:

- `config/biocypher_config.yaml` - BioCypher settings
- `config/schema_config.yaml` - Schema mapping configuration
### Docker Usage

Build and run with Docker:

```bash
docker-compose up -d
```

This will:
1. Build the BioCypher pipeline
2. Start the Neo4j instance
3. Write the data into Neo4j

Access Neo4j at: http://localhost:7474

The pipeline container uses `config/biocypher_config.docker.yaml`, which switches BioCypher to online mode and connects to the Neo4j service. Its password has to match `NEO4J_AUTH` in `docker-compose.yml`.
## Testing

Run the test suite:

```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=synthetic_ppi --cov-report=html
```

## Project Structure

```
synthetic-ppi/
├── config/
│   ├── biocypher_config.yaml
│   ├── biocypher_config.docker.yaml
│   └── schema_config.yaml
├── src/synthetic_ppi/
│   └── adapters/
│       └── synthetic_ppi_adapter.py
├── create_knowledge_graph.py
├── docker-compose.yml
├── Dockerfile
├── tests/
│   └── test_synthetic_ppi_adapter.py
├── pyproject.toml
└── README.md
```

## Development

### Code Style

This project uses:
- **Black** for code formatting
- **isort** for import sorting
- **mypy** for type checking

Format code:
```bash
black .
isort .
```

Type checking:
```bash
mypy src/
```

## License

MIT

## Author

BioCypher User - user@example.com
